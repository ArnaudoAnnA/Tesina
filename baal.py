#based on Matteo Dutto's Movement Recorder https://github.com/MatteoDutto. Thx m8, non e' vero, lo aveva copiato a sua volta, sto terone
import smbus     #import SMBus module of I2C
import time
import collections
import numpy as np
import csv
import sys
import config
import sqlite3
from sqlite3 import Error


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
def init_Fifo(lenFifo, sensorFifo, Athr): #sensorFifo 0=ax 1=ay 2=az 3=mx 4=my 5=mz
    sensorFifo[0] = collections.deque(lenFifo*[0], lenFifo)
    sensorFifo[1] = collections.deque(lenFifo*[0], lenFifo)
    sensorFifo[2] = collections.deque(lenFifo*[0], lenFifo)
    sensorFifo[3] = collections.deque(lenFifo*[0], lenFifo)
    sensorFifo[4] = collections.deque(lenFifo*[0], lenFifo)
    sensorFifo[5] = collections.deque(lenFifo*[0], lenFifo)
    print(list(sensorFifo[5]))
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
    sensor[0] = sensor[0]/16384.0
    sensor[1] = sensor[1]/16384.0
    sensor[2] = sensor[2]/16384.0
    sensor[3] = sensor[3]/131.0
    sensor[4] = sensor[4]/131.0
    sensor[5] = sensor[5]/131.0
    return sensor

#adds an element on each one of the 6 FIFO, automatically deleting the last
def append_sensor_data(sensorFifo, sensor):
    sensorFifo[0].append(sensor[0])
    print sensor
    print sensorFifo
    sensorFifo[1].append(sensor[1])
    sensorFifo[2].append(sensor[2])
    sensorFifo[3].append(sensor[3])
    sensorFifo[4].append(sensor[4])
    sensorFifo[5].append(sensor[5])
    print "after",sensor
    print "after",sensorFifo


#laugero commenta, infame
def db_connect(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print("Error:", e)

#laugero commenta, infame
def get_exercise(conn, exercise_number):
    cur = conn.cursor()
    cur.execute("SELECT * FROM exercises WHERE id=?", str(exercise_number))
    ex = cur.fetchone()
    return ex[config.NAME], ex[config.DESC], ex[config.AUDIO]