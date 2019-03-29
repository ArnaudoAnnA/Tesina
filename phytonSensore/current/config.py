import smbus
#Recorder constants
#FIFO LENGTH
LENFIFO         = 10
#DATA ACQUISITION RATE (n per second)
ACQUIRATE        = 10
#NUMBER OF ELEMENTS OVERLAPPED EVERY FIFO
OVERLAP         = 4
#laugero non sa cosa sia
AUTH            = 0.4
#number of datas sent from each sensor
NDATA           = 6

#defaul address for i2c is 0x68 but if we connect the AD0 pin to VCC it changes to 0x69
Device_Address1 = 0x68  # MPU6050 1 device address
Device_Address2 = 0x69  # MPU6050 2 device address

 # or bus = smbus.SMBus(0) for older version boards