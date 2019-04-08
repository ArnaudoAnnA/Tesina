'''
USAGE: python recorder2Sens.py movement_class acquisitionTime
'''
import time
import collections
import numpy as np
import csv
import sys
import config
import baal
import movementsDictionary
import init2Sens

#Arguments:
#the number of the exercise (keeping in mind the recording of error datasets)
movement_class = sys.argv[1]
#the number of the seconds to record
acquisitionTime = int(sys.argv[2])

#the integer representing the number of instants to record
recordings = acquisitionTime*config.ACQUIRATE
print recordings
#initializing the number of recordings recorded
times = 0
#opening the sqlite db
baal.db_connect(config.DBPATH)
#opening the file writer in order to save the dataset in a csv file named like the exercise
csvfile = open((sys.argv[3] + '.csv'), 'ab')
writer = csv.writer(csvfile)
baal.MPU_Init(config.Device_Address1)
baal.MPU_Init(config.Device_Address2)
#creating the lists that will become FIFO
sensorFifo1=[0]*config.NDATA
sensorFifo2=[0]*config.NDATA
#initializing the FIFO
baal.init_Fifo(config.LENFIFO, sensorFifo1, config.AUTH)
baal.init_Fifo(config.LENFIFO, sensorFifo2, config.AUTH)
#creating the sensor lists
sensor1=[0]*config.LENFIFO
sensor2=[0]*config.LENFIFO
#loop that runs for acquisitionTime time in seconds
print "ciao", 1.0/config.ACQUIRATE
for x in xrange(0, recordings):
    #reading the data from the sensors
    sensor1=baal.read_sensor_data(sensor1, config.Device_Address1)
    sensor2=baal.read_sensor_data(sensor2, config.Device_Address2)
    #parsing the data in an useful format
    sensor1=baal.parse_sensor_data(sensor1)
    sensor2=baal.parse_sensor_data(sensor2)
    #adding the sensor data to the head of the FIFO, automatically deleting the one in the tail
    baal.append_sensor_data(sensorFifo1, sensor1)
    baal.append_sensor_data(sensorFifo2, sensor2)
    #writing the fifo if it has the correct overlap or is the last recording
    if times%(config.LENFIFO-config.OVERLAP)==0 or times==recordings-1 :
        #USA LA LIST DI PYTHON, NON LA LIST DI DEQUE!!!
        writer.writerow(sensorFifo1 + sensorFifo2 + [movement_class])
    #setting next instant
    times=times+1
    time.sleep(1.0/config.ACQUIRATE)
    print 'laugeroMuori' , times 
csvfile.close()
print "finito"