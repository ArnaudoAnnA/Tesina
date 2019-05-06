import smbus

#Recorder constants

#FIFO LENGTH
LENFIFO                  = 10
#DATA ACQUISITION RATE (n per second)
MEASUREMENT_EACH_SECOND  = 25
#NUMBER OF ELEMENTS OVERLAPPED EVERY FIFO
OVERLAP                  = 4
#number of datas sent from each sensor
NDATA_EACH_SENSOR        = 6
#
CSV_PATH                 = "file:///home/pi/Downloads/Tesina-master/phytonSensore/registrazioni/"

#defaul address for i2c is 0x68 but if we connect the AD0 pin to VCC it changes to 0x69
Device_Address1 = 0x68  # MPU6050 ARM device address
Device_Address2 = 0x69  # MPU6050 LEG device address

#PIN associati ai bottoni della mascherina
PIN_BOTTONE_DESTRA = 21
PIN_BOTTONE_CENTRALE = 20
PIN_BOTTONE_SINISTRA = 16

