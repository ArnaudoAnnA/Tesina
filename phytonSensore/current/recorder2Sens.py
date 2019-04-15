'''
USAGE: python recorder2Sens.py movement_class acquisitionTime
'''

#paolo devi sisemare la roba dei file e fare più che non stampino malen e deuqe e quelle puttanate lì

import time
import collections
import numpy as np
import csv
import sys
import config
import baal
import init2Sens

#Arguments:
#the number of the exercise (keeping in mind the recording of error datasets)
movement_class = sys.argv[1]
#the number of the seconds to record
acquisitionTime = int(sys.argv[2])
#constants:
SLEEPTIME = 1.0 / config.ACQUIRATE

#the integer representing the number of instants to record
recordings = acquisitionTime * config.ACQUIRATE
#initializing the number of recordings recorded
times = 0

#opening the sqlite db
baal.db_connect(config.DBPATH)

#opening the file writer in order to save the dataset in a csv file named like the exercise
armSensorFile = open(ArmFile, 'ab')
legSensorFile = open(LegFile, 'ab')
armWriter = csv.writer(armSensorFile)
legWriter = csv.writer(legSensorFile)

#creating the lists that will become FIFO
armSensorFifo = [0] * config.NDATA
legSensorFifo = [0] * config.NDATA

#initializing the FIFO
baal.init_Fifo(config.LENFIFO, armSensorFifo)
baal.init_Fifo(config.LENFIFO, legSensorFifo)

#creating the sensor lists
armSensor = [0] * config.LENFIFO
legSensor = [0] * config.LENFIFO

#loop that runs for acquisitionTime time in seconds
for x in xrange(0, recordings):
	#time at the start of each loop
    oldnow=time.time()
    
    #reading the data from the sensors
    armSensor=baal.read_sensor_data(armSensor, config.Device_Address1)
    legSensor=baal.read_sensor_data(legSensor, config.Device_Address2)
    
    #parsing the data in an useful format
    armSensor=baal.parse_sensor_data(armSensor)
    legSensor=baal.parse_sensor_data(legSensor)
    
    #adding the sensor data to the head of the FIFO, automatically deleting the one in the tail
    baal.append_sensor_data(armSensorFifo, armSensor)
    baal.append_sensor_data(legSensorFifo, legSensor)
    
    
    #writing the fifo if it has the correct overlap or is the last recording
    if times%(config.LENFIFO-config.OVERLAP) == 0 or times == recordings - 1 :
        armWriter.writerow(collections.list(armSensorFifo) + [movement_class])
        legWriter.writerow(collections.list(legSensorFifo) + [movement_class])
        
    #setting next instant
    times = times + 1
    #if throws error, it's because config.ACQUIRATE is too big
    time.sleep(SLEEPTIME - (time.time() - oldnow))

armSensorFile.close()
legSensorFile.close()