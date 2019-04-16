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


def read_raw_data(addr, Device_Address):
    #Accel and Gyro value are 16-bit
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)

    #concatenate higher and lower value
    value = ((high << 8) | low)

    #to get signed value from MPU6050
    if(value > 32768):
        value = value - 65536
    return value

#Creates 6 FIFO, one for each data recived from the MPU6050
def init_Fifo(lenFifo, sensorFifo): #sensorFifo 0=ax 1=ay 2=az 3=mx 4=my 5=mz
    sensorFifo[0] = collections.deque(lenFifo*[0], lenFifo)
    sensorFifo[1] = collections.deque(lenFifo*[0], lenFifo)
    sensorFifo[2] = collections.deque(lenFifo*[0], lenFifo)
    sensorFifo[3] = collections.deque(lenFifo*[0], lenFifo)
    sensorFifo[4] = collections.deque(lenFifo*[0], lenFifo)
    sensorFifo[5] = collections.deque(lenFifo*[0], lenFifo)
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
