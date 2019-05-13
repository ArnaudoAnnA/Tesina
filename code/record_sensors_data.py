# coding=utf-8

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

def acquisition_phase(id_exercise, unset_timer):
	semaphore = thread_semaphore.Semaphore()
	record_sensors_data(id_exercise, semaphore)
	exercise_acquisition_audio(unset_timer, semaphore)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	

def record_sensors_data(id_exercise, semaphore):
	"""function that starts one thread for each sensor. Each thread will read data from sensor and write it on a csv file.
		Threads are controlled by a semaphore"""

	#init sensors
	threadSensor1 = sensor_functions.Thread_sensor_to_csv(config.Device_Address1, config.SENSORPOSITION_LEGSX, movement_class)
	threadSensor2 = sensor_functions.Thread_sensor_to_csv(config.Device_Address2, config.SENSORPOSITION_ARMSX, movement_class)

	threadSensor1.start(semaphore)
	threadSensor2.start(semaphore)

	threadSensor1.join()
	threadSensor2.join()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def exercise_acquisition_audio(unset_timer, semaphore):
	"""function than manages the timer during the acquisition phase and a semaphore.
		The semaphore is controlled by the timer:
		-	when the initial cuntdown finishes the semaphore is unlocked
		- 	when the main cuntdown finishes the semaphore is locked (to stops other threads) """

    output_interface.output_audio(audio_files.DIRECTORY_PATH, [audio_files.REGISTRATION_WILL_START_IN, audio_files.NUMBERS[TIME_BEFORE_START], audio_files.SECONDI])

    #INITIAL CUNTOWN
    registration_countdown = audioTimer.Timer(TIME_BEFORE_START)
    registration_countdown.audio_countdown(1)

    output_interface.audio_output(audio_files.DIRECTORY_PATH, [faudio_files.GO])
    time.sleep(1)

    #UNLOCK
    semaphore.unlock()

    #MAIN CUNTDOWN
    unset_timer.audio_countdown(1)

    #LOCK
    semaphore.lock()

    output_interface.audio_output(audio_files.DIRECTORY_PATH, [audio_files.REGISTRATION_ENDED])
     #volendo qui si può aggiungere una richiesta al'utente se intende salvare l'esercizio appena registrato