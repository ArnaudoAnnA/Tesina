'''
Record movements.
USAGE: python mov_rec.py n_of_movement
'''
import smbus        #import SMBus module of I2C
import time
import collections
import numpy as np
import csv
import sys

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
#defaul address for i2c is 0x68 but if we connect the AD0 pin to VCC it changes to 0x69
bus = smbus.SMBus(1)    # or bus = smbus.SMBus(0) for older version boards
Device_Address1 = 0x68  # MPU6050 1 device address
Device_Address2 = 0x69  # MPU6050 2 device address
#Algorithm constants
LENFIFO   = 10
AUTH 	  = 0.4


MPU_Init()
csvfile = open('movements.csv', 'ab')
writer = csv.writer(csvfile)
sensorFifo1=[]
sensorFifo2=[]
init_Fifo(LENFIFO, sensorFifo1, AUTH)
init_Fifo(LENFIFO, sensorFifo2, AUTH)
sensor1=[0]*LENFIFO
sensor2=[0]*LENFIFO
read_sensor_data(sensor1)
read_sensor_data(sensor2)
parse_sensor_data(sensor1)
parse_sensor_data(sensor2)
append_sensor_data(sensorFifo1, sensor1)
append_sensor_data(sensorFifo2, sensor2)

movement_class = sys.argv[1] 
if not(movement_class):
    movement_class = 'UNK'

while True:
    writer.writerow(list(sensorFifo1) + list(sensorFifo2) + [movement_class])
    #print 'Gx=%.2f, Gy=%.2f, Gz=%.2f, Ax=%.2f, Ay=%.2f, Az=%.2f' %(Gx,Gy,Gz,Ax,Ay,Az)	
    time.sleep(0.2)

close(csvfile)



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


def read_raw_data(addr, Device_Address):
    #Accelero and Gyro value are 16-bit
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)

    #concatenate higher and lower value
    value = ((high << 8) | low)

    #to get signed value from mpu6050
    if(value > 32768):
        value = value - 65536
    return value


def init_Fifo(lenFifo, sensorFifo, Athr): #sensorFifo 0=ax 1=ay 2=az 3=mx 4=my 5=mz

	print (" Reading Data of Gyroscope and Accelerometer")
	sensorFifo[0] = collections.deque(lenFifo*[0], lenFifo)
	sensorFifo[1] = collections.deque(lenFifo*[0], lenFifo)
	sensorFifo[2] = collections.deque(lenFifo*[0], lenFifo)
	sensorFifo[3] = collections.deque(lenFifo*[0], lenFifo)
	sensorFifo[4] = collections.deque(lenFifo*[0], lenFifo)
	sensorFifo[5] = collections.deque(lenFifo*[0], lenFifo)
	return sensorFifo


    #Read Accelerometer raw value
def read_sensor_data(sensor): #sensor 0=ax 1=ay 2=az 3=mx 4=my 5=mz
    sensor[0] = read_raw_data(ACCEL_XOUT_H, Device_Address1)
    sensor[1] = read_raw_data(ACCEL_YOUT_H, Device_Address1)
    sensor[2] = read_raw_data(ACCEL_ZOUT_H, Device_Address1)

    #Read Gyroscope raw value
    sensor[3] = read_raw_data(GYRO_XOUT_H, Device_Address1)
    sensor[4] = read_raw_data(GYRO_YOUT_H, Device_Address1)
    sensor[5] = read_raw_data(GYRO_ZOUT_H, Device_Address1)
    return sensor

def parse_sensor_data(sensor): #sensor 0=ax 1=ay 2=az 3=mx 4=my 5=mz
    #Full scale range +/- 250 degree/C as per sensitivity scale factor
    sensor[0] = sensor[0]/16384.0
    sensor[1] = sensor[1]/16384.0
    sensor[2] = sensor[2]/16384.0


    sensor[3] = sensor[3]/131.0
    sensor[4] = sensor[4]/131.0
    sensor[5] = sensor[5]/131.0
    return sensor

def append_sensor_data(sensorFifo, sensor):
    sensorFifo[0].append(sensor[0])
    sensorFifo[1].append(sensor[1])
    sensorFifo[2].append(sensor[2])
    sensorFifo[3].append(sensor[3])
    sensorFifo[4].append(sensor[4])
    sensorFifo[5].append(sensor[5])
