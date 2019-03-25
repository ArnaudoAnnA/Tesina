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


def MPU_Init():
    #write to sample rate register
    bus.write_byte_data(Device_Address1, SMPLRT_DIV, 7)
    bus.write_byte_data(Device_Address2, SMPLRT_DIV, 7)

    #write to power management register
    bus.write_byte_data(Device_Address1, PWR_MGMT_1, 1)
    bus.write_byte_data(Device_Address2, PWR_MGMT_1, 1)

    #write to Configuration register
    bus.write_byte_data(Device_Address1, CONFIG, 0)
    bus.write_byte_data(Device_Address2, CONFIG, 0)

    #write to Gyro configuration register
    bus.write_byte_data(Device_Address1, GYRO_CONFIG, 24)
    bus.write_byte_data(Device_Address2, GYRO_CONFIG, 24)

    #write to interrupt enable register
    bus.write_byte_data(Device_Address1, INT_ENABLE, 1)
    bus.write_byte_data(Device_Address2, INT_ENABLE, 1)


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

MPU_Init()

print (" Reading Data of Gyroscope and Accelerometer")

LenFifo = 10
Athr = 0.04
Ax1Fifo = collections.deque(LenFifo*[0], LenFifo)
Ay1Fifo = collections.deque(LenFifo*[0], LenFifo)
Az1Fifo = collections.deque(LenFifo*[0], LenFifo)
Gx1Fifo = collections.deque(LenFifo*[0], LenFifo)
Gy1Fifo = collections.deque(LenFifo*[0], LenFifo)
Gz1Fifo = collections.deque(LenFifo*[0], LenFifo)

Ax2Fifo = collections.deque(LenFifo*[0], LenFifo)
Ay2Fifo = collections.deque(LenFifo*[0], LenFifo)
Az2Fifo = collections.deque(LenFifo*[0], LenFifo)
Gx2Fifo = collections.deque(LenFifo*[0], LenFifo)
Gy2Fifo = collections.deque(LenFifo*[0], LenFifo)
Gz2Fifo = collections.deque(LenFifo*[0], LenFifo)

csvfile = open('movements.csv', 'ab')
writer = csv.writer(csvfile)

movement_class = sys.argv[1] 
if not(movement_class):
    movement_class = 'UNK'

while True:
    #Read Accelerometer raw value
    acc_x_1 = read_raw_data(ACCEL_XOUT_H, Device_Address1)
    acc_y_1 = read_raw_data(ACCEL_YOUT_H, Device_Address1)
    acc_z_1 = read_raw_data(ACCEL_ZOUT_H, Device_Address1)

    acc_x_2 = read_raw_data(ACCEL_XOUT_H, Device_Address2)
    acc_y_2 = read_raw_data(ACCEL_YOUT_H, Device_Address2)
    acc_z_2 = read_raw_data(ACCEL_ZOUT_H, Device_Address2)

    #Read Gyroscope raw value
    gyro_x_1 = read_raw_data(GYRO_XOUT_H, Device_Address1)
    gyro_y_1 = read_raw_data(GYRO_YOUT_H, Device_Address1)
    gyro_z_1 = read_raw_data(GYRO_ZOUT_H, Device_Address1)

    gyro_x_2 = read_raw_data(GYRO_XOUT_H, Device_Address2)
    gyro_y_2 = read_raw_data(GYRO_YOUT_H, Device_Address2)
    gyro_z_2 = read_raw_data(GYRO_ZOUT_H, Device_Address2)

    #Full scale range +/- 250 degree/C as per sensitivity scale factor
    Ax1 = acc_x_1/16384.0
    Ay1 = acc_y_1/16384.0
    Az1 = acc_z_1/16384.0

    Ax2 = acc_x_2/16384.0
    Ay2 = acc_y_2/16384.0
    Az2 = acc_z_2/16384.0

    Gx1 = gyro_x_1/131.0
    Gy1 = gyro_y_1/131.0
    Gz1 = gyro_z_1/131.0

    Gx2 = gyro_x_2/131.0
    Gy2 = gyro_y_2/131.0
    Gz2 = gyro_z_2/131.0

    Ax1Fifo.append(Ax1)
    Ay1Fifo.append(Ay1)
    Az1Fifo.append(Az1)
    Gx1Fifo.append(Gx1)
    Gy1Fifo.append(Gy1)
    Gz1Fifo.append(Gz1)

    Ax2Fifo.append(Ax2)
    Ay2Fifo.append(Ay2)
    Az2Fifo.append(Az2)
    Gx2Fifo.append(Gx2)
    Gy2Fifo.append(Gy2)
    Gz2Fifo.append(Gz2)

    movement_detected = (np.abs(Ax1Fifo[LenFifo-1]-Ax1Fifo[LenFifo-2])>Athr) | (np.abs(Ay1Fifo[LenFifo-1]-Ay1Fifo[LenFifo-2])>Athr) | (np.abs(Az1Fifo[LenFifo-1]-Az1Fifo[LenFifo-2])>Athr) | (np.abs(Ax2Fifo[LenFifo-1]-Ax2Fifo[LenFifo-2])>Athr) | (np.abs(Ay2Fifo[LenFifo-1]-Ay2Fifo[LenFifo-2])>Athr) | (np.abs(Az2Fifo[LenFifo-1]-Az2Fifo[LenFifo-2])>Athr)

    if movement_detected:
        #print '%.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f' %(time.time(),Gx,Gy,Gz,Ax,Ay,Az)
        #vengono scritti rispettivamente in sequenza su ogni riga: - il tempo
        #                                                           - le accelerazioni sui 3 assi del primo sensore
        #                                                           - i dati del giroscopio sui 3 assi del primo sensore
        #                                                           - le accelerazioni sui 3 assi del secondo sensore
        #                                                           - i dati del giroscopio sui 3 assi del secondo sensore
        #                                                           - la classe del movimento
        writer.writerow([time.time()] + list(Ax1Fifo) + list(Ay1Fifo) + list(Az1Fifo) + list(Gx1Fifo) + list(Gy1Fifo) + list(Gz1Fifo) + list(Ax2Fifo) + list(Ay2Fifo) + list(Az2Fifo) + list(Gx2Fifo) + list(Gy2Fifo) + list(Gz2Fifo) + [movement_class])
        #print 'Gx=%.2f, Gy=%.2f, Gz=%.2f, Ax=%.2f, Ay=%.2f, Az=%.2f' %(Gx,Gy,Gz,Ax,Ay,Az)	

    time.sleep(0.2)

close(csvfile)
