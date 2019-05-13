# -*- coding: utf-8 -*-
#Python 2
# coding=utf-8

import db_functions as db
import sensor_functions as sf
import thread_semaphore as ts
import audio_timer_set 
import config as c
import audio_raspberry as output_interface
import audio_files_ita as audio_files

SETTING_COMPLETED		= config.REGISTRATION_SETTING_COMPLETED
SENSORPOSITION_LEGSX	= config.SENSORPOSITION_LEGSX
SENSORPOSITION_LEGDX	= config.SENSORPOSITION_LEGDX
SENSORPOSITION_ARMSX	= config.SENSORPOSITION_ARMSX
SENSORPOSITION_ARMDX	= config.SENSORPOSITION_ARMDX

#selecting exercise
output_interface.output_audio([audio_files.ID_EXERCISE_SETTINGS_BEGIN])
settingExercise = audio_timer_set.Thread_get_number_from_user()
settingExercise.start()

settingExercise.join() #while the other threads work, I wait for the result



#selecting exercise time (using the same class)
output_interface.output_audio([audio_files.TIMER_SETTINGS_BEGIN])
settingTimer = audio_timer_set.Thread_get_number_from_user()
settingTimer.start()
settingTimer.join() #while the other threads work, I wait for the result

acquisition_phase(settingExercise.get_number(), settingTimer.timer_object)


#---------------------------------------------------------------------------------------------------------------------------------------

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
