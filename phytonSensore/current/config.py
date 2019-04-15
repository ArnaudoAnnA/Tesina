import smbus

#DB Constants
DBPATH  = "brian.db"
NAME  = 1
DESC  = 2
AUDIO = 3

#Recorder constants

#FIFO LENGTH
LENFIFO         = 10
#DATA ACQUISITION RATE (n per second)
ACQUIRATE       = 25
#NUMBER OF ELEMENTS OVERLAPPED EVERY FIFO
OVERLAP         = 4
#number of datas sent from each sensor
NDATA           = 6

#defaul address for i2c is 0x68 but if we connect the AD0 pin to VCC it changes to 0x69
Device_Address1 = 0x68  # MPU6050 ARM device address
Device_Address2 = 0x69  # MPU6050 LEG device address

#files for sensor datas
LegFile = "leg.csv"
ArmFile = "arm.csv"