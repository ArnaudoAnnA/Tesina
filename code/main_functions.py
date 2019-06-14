#coding: utf-8


import config
import time
import thread_semaphore as ts
import ai_functions as ai
import sensor_functions as sf
import db_functions as db
import button_interface as bi
import vocal_synthesizer as output_interface
import lang
import audio_countdown
from exercise_correctness_observer import Exercise_correctness_observer


CUNTDOWN_BEFORE_START		= config.CUNTDOWN_BEFORE_START
SENSORPOSITION_LEGSX	        = config.SENSORPOSITION_LEGSX
SENSORPOSITION_ARMSX	        = config.SENSORPOSITION_ARMSX
ARMSX_ADDRESS			= config.ARMSX_ADDRESS
LEGSX_ADDRESS			= config.LEGSX_ADDRESS

EXERCISE_DONE_WITH              = lang.dictionary["EXERCISE_DONE_WITH"]
PERCENTAGE_OF_CORRECTNESS       = lang.dictionary["PERCENTAGE_OF_CORRECTNESS"]




#globals
AI_sensor_legsx = None
AI_sensor_armsx = None


def init_sensors():
        sf.init_device()

def init_vocal_synthesizer():
        output_interface.init()

def init_ai(sensor_position):
        ai_sensor = ai.TheBrain(sensor_position)
        ai_sensor.deserialize()
        return ai_sensor

def new_ai(sensor_position):
        ai_sensor = ai.TheBrain(sensor_position)
        return ai_sensor

def select_seconds():
	#getting a list with all options
	list_seconds = lang.dictionary["TIME_DICTIONARY"]
        list_seconds = lang.dict_values_sorted(list_seconds)
	
	#starting function that manage button interface to allow user to select from the list
	output_interface.output(lang.dictionary["TIMER_SETTINGS_BEGIN"]) 
	select_from_list_state = bi.Selecting_from_list_state(list_seconds)
	get_seconds = bi.Button_interface(select_from_list_state)
	get_seconds.set_pins_and_start()
	
	#retriving the selected option
	index = get_seconds.return_value
	seconds = sorted(lang.dictionary["TIME_DICTIONARY"])[index]
	
	return seconds

def _select_exercise(minimum_index = 1):
	#getting all avaiable exercises
	db_exercises = db.Database()
	table_exercises = db_exercises.table_exercises
	exercises = table_exercises.get_all_exercises()
	#print(exercises)
	
	#getting a list with all exercises names (to be passed as a list to scroll by buttons)
	name_column_index = table_exercises.get_column_index(table_exercises.COLUMN_NAME)
	exercises_names = [ exercise[name_column_index] for exercise in exercises ]
	
	#starting function that manage button interface to allow user to select an exercise
	output_interface.output(lang.dictionary["SELECT_THE_EXERCISE"])
	time.sleep(2.0)
	select_from_list_state = bi.Selecting_from_list_state(exercises_names, minimum_index)
	get_exercise = bi.Button_interface(select_from_list_state)
	get_exercise.set_pins_and_start()
	
	#retriving the selected exercise
	selected_index = get_exercise.return_value
	selected_exercise = exercises[selected_index]
	selected_exercise_id = selected_exercise[table_exercises.get_column_index(table_exercises.COLUMN_ID_EXERCISE)]
	
	return selected_exercise_id	#I return the id of the selected exercise tuple

def select_exercise_to_do():
        return _select_exercise()
        
def select_exercise_to_record():
        return _select_exercise(0)
        


def select_new_exercise_id():
	#starting function that allow user to select a number using buttons
	output_interface.output(lang.dictionary["ID_EXERCISE_SETTINGS_BEGIN"])
	setting_number_state = bi.Setting_number_state()
	get_number = bi.Button_interface(setting_number_state)
	get_number.set_pins_and_start()
	
	return get_number.return_value



def do_exercise(id_exercise, seconds, legsx_AI_object, armsx_AI_object):       
        #Preparing threads.
	#Each thread takes data from a sensor and send it to the relative AI object.
	#Each AI object has the same observer. The observer object is notifyed when an AI object get a new result.
	#The observer stores the result and then calls a method to give it output.
	#So the observer will store data from all threads and, when threads exit, will know the average correctness of the exercise.
        semaphore = ts.Semaphore()
        observer = Exercise_correctness_observer() #the object where I will store all the percentage of correctness returned by ai
	thread_legsx = sf.Sensor_to_ai_thread(LEGSX_ADDRESS, SENSORPOSITION_LEGSX, legsx_AI_object, id_exercise, semaphore, observer)
	thread_armsx = sf.Sensor_to_ai_thread(ARMSX_ADDRESS, SENSORPOSITION_ARMSX, armsx_AI_object, id_exercise, semaphore, observer)


	#threads will start when semaphore unloks
        thread_legsx.start()
        thread_armsx.start()


	#cuntdown before start
	output_interface.output(lang.dictionary["REGISTRATION_WILL_START_IN"])	# "REGISTRATION WILL START IN X SECONDS"
        audio_countdown.start(CUNTDOWN_BEFORE_START)
	output_interface.output(lang.dictionary["GO"])	# "go"

	#unlocking threads
        semaphore.unlock()

        #wait the end of the exercise
        time.sleep(seconds)


        #stopping threads
        semaphore.lock()
        thread_legsx.join()
        thread_armsx.join()

        #final report
        average = EXERCISE_DONE_WITH + str(int(observer.get_correctness_average())) + PERCENTAGE_OF_CORRECTNESS
        output_interface.output(average)
        time.sleep(10.0)

def record_exercise(id_exercise, seconds):
	#preparing threads
        semaphore = ts.Semaphore()
	thread_legsx = sf.Sensor_to_csv_thread(LEGSX_ADDRESS, SENSORPOSITION_LEGSX, id_exercise, semaphore)
	thread_armsx = sf.Sensor_to_csv_thread(ARMSX_ADDRESS, SENSORPOSITION_ARMSX, id_exercise, semaphore)

	#threads will start when semaphore unloks
	thread_legsx.start()
        thread_armsx.start()
	
	#cuntdown before start 
	output_interface.output(lang.dictionary["REGISTRATION_WILL_START_IN"])	# "REGISTRATION WILL START IN X SECONDS"
	audio_countdown.start(CUNTDOWN_BEFORE_START)
	output_interface.output(lang.dictionary["GO"])

	#unlocking threads
        semaphore.unlock()

	#wait the end of the exercise
        time.sleep(seconds)
	#stopping threads
	semaphore.lock()
        thread_legsx.join()
        thread_armsx.join()
	output_interface.output(lang.dictionary["REGISTRATION_ENDED"])	# "registration ended"

