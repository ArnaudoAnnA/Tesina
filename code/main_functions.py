#coding: utf-8


import config
import thread_semaphore as ts
import ai_functions as ai
import sensor_functions as sf
import db_functions as db
import _button_interface_for_test as bi
import _test_output as output_interface
import lang
import audio_countdown
from exercise_correctness_observer import Exercise_correctness_observer


CUNTDOWN_BEFORE_START		= config.CUNTDOWN_BEFORE_START
SENSORPOSITION_LEGSX	        = config.SENSORPOSITION_LEGSX
SENSORPOSITION_ARMSX	        = config.SENSORPOSITION_ARMSX
ARMSX_ADDRESS			= config.ARMSX_ADDRESS
LEGSX_ADDRESS			= config.LEGSX_ADDRESS



#globals
AI_sensor_legsx = None
AI_sensor_armsx = None


def init_sensor_vocal_synthesizer():
        sf.init_device()
	output_interface.init_vocal_synthesizer()

def init_ai():
	global AI_sensor_legsx
	global AI_sensor_armsx

        AI_sensor_legsx = ai.TheBrain(SENSORPOSITION_LEGSX)
        #AI_sensor_armsx = ai.TheBrain(SENSORPOSITION_ARMSX)
        AI_sensor_legsx.deserialize()
        #AI_sensor_armsx.deserialize()

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
	seconds = get_seconds.return_value
	
	return seconds
	
def select_exercise():
	#getting all avaiable exercises
	db_exercises = db.Database()
	table_exercises = db_exercises.table_exercises
	exercises = table_exercises.get_all_exercises()
	print(exercises)
	
	#getting a list with all exercises names (to be passed as a list to scroll by buttons)
	name_column_index = table_exercises.get_column_index(table_exercises.COLUMN_NAME)
	exercises_names = [ exercise[name_column_index] for exercise in exercises ]
	
	#starting function that manage button interface to allow user to select an exercise
	output_interface.output(lang.dictionary["SELECT_THE_EXERCISE"])
	select_from_list_state = bi.Selecting_from_list_state(exercises_names)
	get_exercise = bi.Button_interface(select_from_list_state)
	get_exercise.set_pins_and_start()
	
	#retriving the selected exercise
	selected_index = get_exercise.return_value
	selected_exercise = exercises[selected_index]
	
	return selected_exercise	#I return the id of the selected exercise tuple


def select_new_exercise_id():
	#starting function that allow user to select a number using buttons
	output_interface.output(lang.dictionary["ID_EXERCISE_SETTINGS_BEGIN"])
	setting_number_state = bi.Setting_number_state()
	get_number = bi.Button_interface(setting_number_state)
	get_number.set_pins_and_start()
	
	return get_number.return_value



def do_exercise(id_exercise, seconds):       
	global AI_sensor_legsx
	global AI_sensor_armsx

        #Preparing threads.
	#Each thread takes data from a sensor and send it to the relative AI object.
	#Each AI object has the same observer. The observer object is notifyed when an AI object get a new result.
	#The observer stores the result and then calls a method to give it output.
	#So the observer will store data from all threads and, when threads exit, will know the average correctness of the exercise.
        semaphore = ts.Semaphore()
        observer = Exercise_correctness_observer() #the object where I will store all the percentage of correctness returned by ai
	thread_legsx = sf.Sensor_to_ai_thread(LEGSX_ADDRESS, SENSORPOSITION_LEGSX, AI_sensor_legsx, id_exercise, semaphore, observer)
	#thread_armsx = sf.Sensor_to_ai_thread(ARMSX_ADDRESS, SENSORPOSITION_ARMSX, AI_sensor_armsx, id_exercise, semaphore, observer)


	#threads will start when semaphore unloks
        thread_legsx.start()
        #thread_armsx.start()


	#cuntdown before start
	output_interface.output(lang.dictionary["REGISTRATION_WILL_START_IN"]+" "+str(CUNTDOWN_BEFORE_START)+" "+lang.dictionary["SECONDS"])	# "REGISTRATION WILL START IN X SECONDS"
        audio_countdown.start(CUNTDOWN_BEFORE_START)
	output_interface.output(lang.dictionary["GO"])	# "go"

	#unlocking threads
        semaphore.unlock()

        #contdown during the execution of the exercise
        audio_countdown.start(seconds)


        #stopping threads
        semaphore.lock()
        thread_legsx.join()
        #thread_armsx.join()

        #final report
        output_interface.output(observer.get_correctness_average())


def record_exercise(id_exercise, seconds):
	#preparing threads
        semaphore = ts.Semaphore()
	thread_legsx = sf.Sensor_to_csv_thread(LEGSX_ADDRESS, SENSORPOSITION_LEGSX, id_exercise, semaphore)
	#thread_armsx = sf.Sensor_to_csv_thread(ARMSX_ADDRESS, SENSORPOSITION_ARMSX, id_exercise, semaphore)

	#threads will start when semaphore unloks
	thread_legsx.start()
        #thread_armsx.start()
	
	#cuntdown before start 
	output_interface.output(lang.dictionary["REGISTRATION_WILL_START_IN"]+" "+str(CUNTDOWN_BEFORE_START)+" "+lang.dictionary["SECONDS"])	# "REGISTRATION WILL START IN X SECONDS"
	audio_countdown.start(CUNTDOWN_BEFORE_START)
	output_interface.output(lang.dictionary["GO"])	# "go"

	#unlocking threads
        semaphore.unlock()

	#cuntdown during the registration of the exercise
	audio_countdown.start(seconds)

	#stopping threads
	semaphore.lock()
        thread_legsx.join()
        #thread_armsx.join()
	output_interface.output(lang.dictionary["REGISTRATION_ENDED"])	# "registration ended"

	#QUI SI POTREBBE CHIEDERE CONFERMA ALL'UTENTE SE VUOLE SALVARE L'ESERCIZIO (OPPURE LO HA FATTO MALISSIMO E QUINDI NON LO VUOLE SALVARE)

