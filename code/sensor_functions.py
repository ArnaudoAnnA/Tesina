# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------------------------------------
#   funzioni:
#   -   MPU_init            -> inizializzazione sensore
#   -   read_raw_data       -> leggere un singolo dato da un sensore in un dato istante
#   -   init_Fifo           -> (da rivedere, non rispetta architettura multithread) inizializza liste
#   -   read_sensor_data    -> legge tutti i dati provenienti da un MPU in un dato istante
#   -   parse_sensor_data   -> parsifica i dati ricevuti da un MPU
#   -   append_sensor_data  -> aggiunge alla coda fifo i dati ricevuti da un MPU

#   NOTA: un MPU è composto da più sensori

#-------------------------------------------------------------------------------------------------------------

#based on Matteo Dutto's Movement Recorder https://github.com/MatteoDutto.
import smbus     #import SMBus module of I2C
import time
import collections
import numpy as np
import csv
import sys
import config
import threading
import thread_semaphore

MEASUREMENT_EACH_SECOND     = config.MEASUREMENT_EACH_SECOND
NDATA_EACH_SENSOR           = config.NDATA_EACH_SENSOR
LENFIFO                     = config.LENFIFO
OVERLAP                     = config.OVERLAP
CSV_FILE_PATH               = config.CSV_FILE_PATH
LEGSX_ADDRESS               = config.LEGSX_ADDRESS 
ARMSX_ADDRESS               = config.ARMSX_ADDRESS


#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47
bus = smbus.SMBus(1)

ACCEL_PARSE_NUMBER = 16384.0
GYRO_PARSE_NUMBER = 131.0

def MPU_Init(Device_Address):
    #write to sample rate register
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)

    #write to power management register
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)

    #write to Configuration register
    bus.write_byte_data(Device_Address, CONFIG, 0)

    #write to Gyro configuration register
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)

    #write to interrupt enable register
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def init_device():
    MPU_Init(ARMSX_ADDRESS)
    MPU_Init(LEGSX_ADDRESS)

def read_raw_data(addr, Device_Address):
    #Accel and Gyro value are 16-bit
    high = bus.read_byte_data(Device_Address, addr)
    low  = bus.read_byte_data(Device_Address, addr + 1)

    #concatenate higher and lower value
    value = ((high << 8) | low)

    #to get signed value from MPU6050
    if(value > 32768):
        value = value - 65536
    return value

#Creates 6 FIFO, one for each data recived from the MPU6050
def init_Fifo(lenFifo, sensorFifo): #sensorFifo 0=ax 1=ay 2=az 3=mx 4=my 5=mz
    sensorFifo[0] = collections.deque(lenFifo * [0], lenFifo)
    sensorFifo[1] = collections.deque(lenFifo * [0], lenFifo)
    sensorFifo[2] = collections.deque(lenFifo * [0], lenFifo)
    sensorFifo[3] = collections.deque(lenFifo * [0], lenFifo)
    sensorFifo[4] = collections.deque(lenFifo * [0], lenFifo)
    sensorFifo[5] = collections.deque(lenFifo * [0], lenFifo)
    return sensorFifo

#Read Accelerometer raw value
def read_sensor_data(sensor, Device_Address): #sensor 0=ax 1=ay 2=az 3=mx 4=my 5=mz
    sensor[0] = read_raw_data(ACCEL_XOUT_H, Device_Address)
    sensor[1] = read_raw_data(ACCEL_YOUT_H, Device_Address)
    sensor[2] = read_raw_data(ACCEL_ZOUT_H, Device_Address)

    #Read Gyroscope raw value
    sensor[3] = read_raw_data(GYRO_XOUT_H, Device_Address)
    sensor[4] = read_raw_data(GYRO_YOUT_H, Device_Address)
    sensor[5] = read_raw_data(GYRO_ZOUT_H, Device_Address)
    return sensor

def parse_sensor_data(sensor): #sensor 0=ax 1=ay 2=az 3=mx 4=my 5=mz
    #Full scale range +/- 250 degree/C as per sensitivity scale factor
    sensor[0] = sensor[0] / ACCEL_PARSE_NUMBER
    sensor[1] = sensor[1] / ACCEL_PARSE_NUMBER
    sensor[2] = sensor[2] / ACCEL_PARSE_NUMBER
    sensor[3] = sensor[3] / GYRO_PARSE_NUMBER
    sensor[4] = sensor[4] / GYRO_PARSE_NUMBER
    sensor[5] = sensor[5] / GYRO_PARSE_NUMBER
    return sensor

#adds an element on each one of the 6 FIFO, automatically deleting the last
def append_sensor_data(sensorFifo, sensor):
    sensorFifo[0].append(sensor[0])
    sensorFifo[1].append(sensor[1])
    sensorFifo[2].append(sensor[2])
    sensorFifo[3].append(sensor[3])
    sensorFifo[4].append(sensor[4])
    sensorFifo[5].append(sensor[5])
    
def toList_Fifo(fifo):
    ret = []

    for i in xrange(0, len(fifo)):
        ret = ret + list(fifo[i])
  
    return ret
    
class Read_sensor(threading.Thread):
	"""ABSTRACT CLASS (method run not defined)
		Class that represent a sensor and give methods to read data from that sensor.
	"""	

    device_address              = None
    device_position             = None
    data_one_misuration         = None
    window_misurations_fifo     = None
    
    def __init__(self, device_address, device_position, id_exercise):
    	threading.Thread.__init__(self)
        
        self.device_address = device_address
        self.device_position = device_position 

        #il numero dell'esercizio che questa istanza andrà di thread andrà a memorizzare
        self.id_exercise = id_exercise    
        
        #lista che conterrà tutti i dati registrati dal sensore in un istante
        self.data_one_misuration = [0] * NDATA_EACH_SENSOR
        #lista che contiene i dati registrati dal sensore in una finestra di tempo          
        self.window_misurations_fifo = [0] * NDATA_EACH_SENSOR      
        init_Fifo(LENFIFO, self.window_misurations_fifo)
    
    
    def read_data_and_callback(self, semaphore, callback_when_data_ready):
    	"""read data from the current sensor and call a callback function each time data is ready. 
    		It works while the semaphore is unlocked"""
        times   = 0

        semaphore.waitForUnlock()
        
        while(semaphore.isUnlocked()):

            oldnow = time.time()
            #reading the data from the sensor
            self.data_one_misuration = read_sensor_data(self.data_one_misuration, self.device_address)
            #parsing the data in an useful format
            self.data_one_misuration = parse_sensor_data(self.data_one_misuration)
            #adding the sensor data to the head of the FIFO, automatically deleting the one in the tail
            append_sensor_data(self.window_misurations_fifo, self.data_one_misuration)
            #writing the fifo if it has the correct overlap or is the last recording
            if times % (LENFIFO-OVERLAP) == 0:
                callback_when_data_ready()
            #setting next instant
            times=times+1
            time.sleep(1.0 / MEASUREMENT_EACH_SECOND - (time.time() - oldnow))
            print ('times: ', times) 
        
        print(self.device_position, "DEBUG:  finished")



class Thread_read_sensor_and_write(Read_sensor):
	"""Specialized class for read data from a specific sensor and write it on a csv file.
		It inherits from threading.Thread(), so data sensor can be read and written by a separate thread
		NOTE: the name of the csv file is the position of the sensor"""

	id_exercise                 = None
	csvfile                     = None
	writer                      = None

	def __init__(self, device_address, device_position, id_exercise):
	 	Thread_read_sensor.__init__(self, device_address, device_position, recordings, id_exercise)

        #il file dove verrà salvato l'esercizio ha un nome che rappresenta la posizione del sensore
        self.csvfile = open(CSV_FILE_PATH+device_position+'.csv', 'ab')        
        self.writer = csv.writer(self.csvfile)


    def run(self, semaphore):
    	self.read_data_and_callback(semaphore, self.write_row_on_csv)
    	self.csvfile.close()


    def write_row_on_csv(self):
    	self.writer.writerow(toList_Fifo(self.window_misurations_fifo) + [self.id_exercise])



class Read_sensor_and_IA(Read_sensor):
	"""Specialized class for:
		-	reading data from a sensor
		-	use IA algoritm to retrive percentage of correctness
		- 	notify the user interface that a result is avaiable to be given in output"""
	ia_object = None

	def __init__(self, device_address, device_position, ia_object, id_exercise):
		Thread_read_sensor.__init__(self, device_address, device_position, recordings, id_exercise)
		self.ia_object = ia_object

	def run(self, semaphore):
		self.read_data_and_callback(semaphore, send_data_to_ia)

	def send_data_to_ia(self):
		percentage = ia_object.get_percentage_of_correctness(self.id_exercise, self.window_misurations_fifo)		
		ia_object.observer.ia_result_notify(self.device_position, percentage)
        
