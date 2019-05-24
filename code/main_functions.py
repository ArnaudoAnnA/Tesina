#coding: utf-8



import config
import thread_semaphore as ts
import ai_functions as ai
import sensor_functions as sf
import vocal_syinthesizer as output_interface
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



def do_exercise(id_exercise, seconds):       
	global AI_sensor_legsx
	global AI_sensor_armsx

        #Preparing threads.
	#Each thread takes data from a sensor and send it to the relative AI object.
	#Each AI object has the same observer. The observer object is notifyed when an AI object get a new result.
	#The observer stores the result and then calls a method to give it output.
	#So the observer will store data from all threads and, when threads exit, will know the average correctness of the exercise.
        observer = Exercise_correcness_observer() #the object where I will store all the percentage of correctness returned by ai
	thread_legsx = Sensor_to_ai_thread(LEGSX_ADDRESS, SENSORPOSITION_LEGSX, AI_sensor_legsx, id_exercise, observer)
	thread_armsx = Sensor_to_ai_thread(LEGSX_ADDRESS, SENSORPOSITION_LEGSX, AI_sensor_armsx, id_exercise, observer)


	#threads will start when semaphore unloks
        semaphore = ts.Semaphore()
        thread_legsx.start(semaphore)
        thread_armsx.start(semaphore)


	#cuntdown before start 
        audio_cuntdown.start(START_CUNTDOWN)
	vs.say(lang.dictionary["GO"])

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
	thread_legsx = Thread(target = sf.record_sensor_data, args = (id_exercise, seconds, SENSORPOSITION_LEGSX, LEGSX_ADDRESS))
	thread_armsx = Thread(target = sf.record_sensor_data, args = (id_exercise, seconds, SENSORPOSITION_ARMSX, ARMSX_ADDRESS))

	#threads will start when semaphore unloks
	semaphore = ts.Semaphore()
	thread_legsx.start(semaphore)
        thread_armsx.start(semaphore)

	
	#cuntdown before start 
	audio_cuntdown.start(START_CUNTDOWN)
	vs.say(lang.dictionary["GO"])

	#unlocking threads
        ts.semaphore.unlock()

	#cuntdown during the registration of the exercise
	cuntdown(seconds)

	#stopping threads
	ts.semaphore.lock()
        thread_legsx.join()
        thread_armsx.join()

	#QUI SI POTREBBE CHIEDERE CONFERMA ALL'UTENTE SE VUOLE SALVARE L'ESERCIZIO (OPPURE LO HA FATTO MALISSIMO E QUINDI NON LO VUOLE SALVARE)

