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
import funzioniDB
import funzioniSensori
import init2Sens
import semaforoThread

#Arguments:
movement_class = sys.argv[1] #the number of the exercise (keeping in mind the recording of error datasets)
acquisitionTime = int(sys.argv[2]) #the number of the seconds to record

#the integer representing the number of instants to record
recordings = acquisitionTime*config.LENFIFO
print ("recordings: ",recordings)

#init sensors
threadSensor1 = funzioniSensori.Thread_readSensor(config.Device_Address1, config.SENSORPOSITION_LEGSX, movement_class, recordings)
threadSensor2 = funzioniSensori.Thread_readSensor(config.Device_Address2, config.SENSORPOSITION_ARMSX, movement_class, recordings)

semaforoThread.semaforo.clear() #variabile che serve per fare in modo che tutti i thread partano in contemporanea

threadSensor1.start()
threadSensor2.start()

semaforoThread.semaforo.set()    #I thread iniziano a raccogliere info dai sensori solo da questo momento! 

threadSensor1.join()
threadSensor2.join()