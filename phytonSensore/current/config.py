import smbus





#Recorder constants

#FIFO LENGTH
WINDOW_LENGHT            = 10
#DATA ACQUISITION RATE (n per second)
MEASUREMENT_EACH_SECOND  = 25
#NUMBER OF ELEMENTS OVERLAPPED EVERY FIFO
WINDOW_OVERLAP           = 4
#number of datas sent from each sensor
NDATA_EACH_SENSOR        = 6

#defaul address for i2c is 0x68 but if we connect the AD0 pin to VCC it changes to 0x69
Device_Address1 = 0x68  # MPU6050 ARM device address
Device_Address2 = 0x69  # MPU6050 LEG device address

#PIN associati ai bottoni della mascherina
PIN_BOTTONE_DESTRA = 21
PIN_BOTTONE_CENTRALE = 20
PIN_BOTTONE_SINISTRA = 16

#posizioni in cui si può trovare un sensore
SENSORPOSITION_LEGSX = "legsx"
SENSORPOSITION_LEGDX = "legdx"
SENSORPOSITION_ARMSX = "armsx"
SENSORPOSITION_ARMDX = "armdx"
