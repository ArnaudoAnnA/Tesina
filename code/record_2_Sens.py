# coding=utf-8

'''
USAGE: python recorder2Sens.py movement_class acquisitionTime
'''
import time
import collections
import numpy as np
import csv
import sys
import config
import db_functions
import sensor_functions
import init2Sens
import thread_semaphore

#Arguments:
movement_class = sys.argv[1] #the number of the exercise (keeping in mind the recording of error datasets)
acquisitionTime = int(sys.argv[2]) #the number of the seconds to record

#the integer representing the number of instants to record
recordings = acquisitionTime * config.LENFIFO
print ("recordings: ", recordings)

#init sensors
threadSensor1 = sensor_functions.Thread_readSensor(config.Device_Address1, config.SENSORPOSITION_LEGSX, movement_class, recordings)
threadSensor2 = sensor_functions.Thread_readSensor(config.Device_Address2, config.SENSORPOSITION_ARMSX, movement_class, recordings)

#variable used for starting all threads simultaneosly
semaphore = thread_semaphore.Semaphore()

threadSensor1.start(semaphore)
threadSensor2.start(semaphore)

#threads start to collect data from this moment
semaphore.unlock()

threadSensor1.join()
threadSensor2.join()