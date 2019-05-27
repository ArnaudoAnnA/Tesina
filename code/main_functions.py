#coding: utf-8



import config
import thread_semaphore as ts
import ai_functions as ai
import sensor_functions as sf
import db_functions as db
import button_interface as bi
import vocal_syinthesizer as output_interface
import lang
import audio_cuntdown
from exercise_correctness_observer import Exercise_correcness_observer


START_COUNTDOWN			= config.START_COUNTDOWN
SENSORPOSITION_LEGSX	        = config.SENSORPOSITION_LEGSX
SENSORPOSITION_ARMSX	        = config.SENSORPOSITION_ARMSX
ARMSX_ADDRESS			= config.ARMSX_ADDRESS
LEGSX_ADDRESS			= config.LEGSX_ADDRESS



#globals
AI_sensor_legsx = None
AI_sensor_armsx = None



def init_sensor_vocal_syntetizer():
        sf.init_device()
	vs.init_vocal_synthesizer()

def init_ai():
	global AI_sensor_legsx
	global AI_sensor_armsx

        AI_sensor_legsx = ai_funcions.TheBrain(SENSORPOSITION_LEGSX)
        AI_sensor_armsx = ai_funcions.TheBrain(SENSORPOSITION_ARMDX)
        AI_sensor_legsx.unserialize()
        AI_sensor_armsx.unserialize()

def select_seconds():
	#getting a list with all options
	list_seconds = lang.dictionary["TIME_DICTIONARY"]
        list_seconds = lang.dict_values_sorted(list_seconds)
	
	#starting function that manage button interface to allow user to select from the list
	output_interface.output(lang.dictionary["TIMER_SETTINGS_BEGIN"]) 
	select_from_list_state = bi.Select_from_list_state(list_seconds)
	get_seconds = bi.Button_interface(select_from_list_state)
	
	#retriving the selected option
	seconds = get_seconds.return_value
	
	return seconds
	
def select_exercise():
	#getting all avaiable exercises
	db_exercises = db.Database()
	table_exercises = db_exercises.table_exercises
	exercises = table_exercises.get_all_exercises()
	
	#getting a list with all exercises names (to be passed as a list to scroll by buttons)
	name_column_index = table_exercises.get_column_index()
	exercises_names = [ exercise[name_column_index] for exercise in exercises ]
	
	#starting function that manage button interface to allow user to select an exercise
	ouput_interface.output(lang.dictionary["SELECT_THE_EXERCISE"])
	select_from_list_state = bi.Select_from_list_state(exercises_names)
	get_exercise = bi.Button_interface(select_from_list_state)
	
	#retriving the selected exercise
	selected_index = get_exercise.return_value
	selected_exercise = exercises[selected_index]
	
	return selected_exercise	#I return the id of the selected exercise tuple


def select_new_exercise_id():
	#starting function that allow user to select a number using buttons
	ouput_interface.output(lang.dictionary["ID_EXERCISE_SETTINGS_BEGIN"])
	setting_number_state = bi.Setting_number_state()
	get_number = bi.Button_interface(setting_number_state)
	
	return set_number.return_value



def do_exercise(id_exercise, seconds):       
	global AI_sensor_legsx
	global AI_sensor_armsx

        #Preparing threads.
	#Each thread takes data from a sensor and send it to the relative AI object.
	#Each AI object has the same observer. The observer object is notifyed when an AI object get a new result.
	#The observer stores the result and then calls a method to give it output.
	#So the observer will store data from all threads and, when threads exit, will know the average correctness of the exercise.
        observer = Exercise_correcness_observer() #the object where I will store all the percentage of correctness returned by ai
	thread_legsx = sf.Sensor_to_ai_thread(LEGSX_ADDRESS, SENSORPOSITION_LEGSX, AI_sensor_legsx, id_exercise, observer)
	thread_armsx = sf.Sensor_to_ai_thread(LEGSX_ADDRESS, SENSORPOSITION_LEGSX, AI_sensor_armsx, id_exercise, observer)


	#threads will start when semaphore unloks
        semaphore = ts.Semaphore()
        thread_legsx.start(semaphore)
        thread_armsx.start(semaphore)


	#cuntdown before start
	output_interface.output(lang.dictionary["REGISTRATION_WILL_START_IN"]+" "+START_CUNTDOWN+" "+lang.dictionary["SECONDS"])	# "REGISTRATION WILL START IN X SECONDS"
        audio_cuntdown.start(START_CUNTDOWN)
	output_interface.output(lang.dictionary["GO"])	# "go"

	#unlocking threads
        ts.semaphore.unlock()

        #contdown during the execution of the exercise
        cuntdown(seconds)


        #stopping threads
        ts.semaphore.lock()
        thread_legsx.join()
        thread_armsx.join()

        #final report
        output_interface.output(observer.get_correctness_average())


def record_exercise(id_exercise, seconds):
	#preparing threads
	thread_legsx = sf.Sensor_to_csv_thread(LEGSX_ADDRESS, SENSORPOSITION_LEGSX, id_exercise)
	thread_armsx = sf.Sensor_to_csv_thread(ARMSX_ADDRESS, SENSORPOSITION_ARMSX, id_exercise)

	#threads will start when semaphore unloks
	semaphore = ts.Semaphore()
	thread_legsx.start(semaphore)
        thread_armsx.start(semaphore)
	
	#cuntdown before start 
	output_interface.output(lang.dictionary["REGISTRATION_WILL_START_IN"]+" "+START_CUNTDOWN+" "+lang.dictionary["SECONDS"])	# "REGISTRATION WILL START IN X SECONDS"
	audio_cuntdown.start(START_CUNTDOWN)
	output_interface.output(lang.dictionary["GO"])	# "go"

	#unlocking threads
        ts.semaphore.unlock()

	#cuntdown during the registration of the exercise
	audio_cuntdown.start(seconds)

	#stopping threads
	ts.semaphore.lock()
        thread_legsx.join()
        thread_armsx.join()
	output_interface.output(lang.dictionary["REGISTRATION_ENDED"]	# "registration ended"

	#QUI SI POTREBBE CHIEDERE CONFERMA ALL'UTENTE SE VUOLE SALVARE L'ESERCIZIO (OPPURE LO HA FATTO MALISSIMO E QUINDI NON LO VUOLE SALVARE)

