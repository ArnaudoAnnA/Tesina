'''
Read Gyro and Accelerometer by Interfacing Raspberry Pi with MPU6050 using Python
http://www.electronicwings.com
'''

import smbus                #import SMBus module of I2C
from time import sleep      #import

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

    print ("MPU6050 1: Gx=%.2f" %Gx1, u'\u00b0'+ "/s", "\tGy=%.2f" %Gy1, u'\u00b0'+ "/s", "\tGz=%.2f" %Gz1, u'\u00b0'+ "/s", "\tAx=%.2f g" %Ax1, "\tAy=%.2f g" %Ay1, "\tAz=%.2f g"%Az1)
    print ("MPU6050 2: Gx=%.2f" %Gx2, u'\u00b0'+ "/s", "\tGy=%.2f" %Gy2, u'\u00b0'+ "/s", "\tGz=%.2f" %Gz2, u'\u00b0'+ "/s", "\tAx=%.2f g" %Ax2, "\tAy=%.2f g" %Ay2, "\tAz=%.2f g"%Az2)

    print("\n")

    sleep(1)