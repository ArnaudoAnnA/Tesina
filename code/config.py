# coding=utf-8
import smbus

#Recorder constants
LENFIFO                         = 10				#FIFO LENGTH
MEASUREMENT_EACH_SECOND         = 25				#DATA ACQUISITION RATE (n per second)
OVERLAP                         = 4					#NUMBER OF ELEMENTS OVERLAPPED EVERY FIFO
NDATA_EACH_SENSOR               = 6					#number of datas sent from each sensor


#folder structure
HOME_PATH                       = "/home/pi/Downloads/Tesina-master/"
AI_PATH                         = HOME_PATH+"/files/pkl/"
DB_PATH                         = HOME_PATH+"files/db/"
CSV_PATH                        = HOME_PATH+"files/csv/"
CSV_FILE_PATH                   = "file://"+CSV_PATH


#DB constants
DB_NAME                         = "brian.db"

#AI constants 
#header representing the recorded data row, or csv columns
ID_EXERCISE                     = "id_exercise"		#name of the exercise id column
N_ESTIMATORS                    = 100      			#number of the trees
MAX_DEPTH                       = 3        			#depth of the trees
HEADER_FEATURES                 = ['Ax_' + str(i) for i in xrange(1, LENFIFO+1)]+['Ay_' + str(i) for i in xrange(1, LENFIFO+1)]+['Az_' + str(i) for i in xrange(1, LENFIFO+1)]+['Gx_' + str(i) for i in xrange(1, LENFIFO+1)]+['Gy_' + str(i) for i in xrange(1, LENFIFO+1)]+['Gz_' + str(i) for i in xrange(1, LENFIFO+1)] # data heading
HEADER                          = HEADER_FEATURES + [ID_EXERCISE]


#sensors addess
#defaul address for i2c is 0x68 but if we connect the AD0 pin to VCC it changes to 0x69
ARMSX_ADDRESS                   = 0x68  			# MPU6050 ARM device address
LEGSX_ADDRESS                   = 0x69  			# MPU6050 LEG device address
#ARMDX_ADDRESS 			
#LEGDX_ADDRESS


#sensors names/positions
SENSORPOSITION_LEGSX            = "legsx"
SENSORPOSITION_LEGDX            = "legdx"
SENSORPOSITION_ARMSX            = "armsx"
SENSORPOSITION_ARMDX            = "armdx"

#registration constants
REGISTRATION_TIME_BEFORE_START 	= 5   #cuntdown before start of acquisition


#interface pins addresses
RIGHT_BUTTON_PIN                = 21
CENTRAL_BUTTON_PIN              = 20
LEFT_BUTTON_PIN                 = 16
