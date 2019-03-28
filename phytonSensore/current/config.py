#Recorder constants
#FIFO LENGTH
LENFIFO   		= 10
#DATA ACQUISITION RATE (n per second)
ACQIRATE 		= 10
#NUMBER OF ELEMENTS OVERLAPPED EVERY FIFO
OVERLAP 		= 4

AUTH 	  		= 0.4

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
