#coding: utf-8

import time
import thread_semaphore as ts
import ai_functions as ai
import sensor_functions as sf
import vocal_syinthesizer as output_interface
import config
from exercise_correctness_observer import Exercise_correcness_observer

START_COUNTDOWN			= config.START_COUNTDOWN
SENSORPOSITION_LEGSX	        = config.SENSORPOSITION_LEGSX
SENSORPOSITION_ARMSX	        = config.SENSORPOSITION_ARMSX
ARMSX_ADDRESS			= config.ARMSX_ADDRESS
LEGSX_ADDRESS			= config.LEGSX_ADDRESS


def init_sensor_vocal_syntetizer():
        sf.init_device()
	vs.init_vocal_synthesizer()

def init_ai():
        AI_sensor_legsx = ai_funcions.TheBrain(SENSORPOSITION_LEGSX)
        AI_sensor_armsx = ai_funcions.TheBrain(SENSORPOSITION_ARMDX)
        AI_sensor_legsx.unserialize()
        AI_sensor_armsx.unserialize()

def do_exercise(id_exercise, seconds, aiLegsx, aiArmsx):        #TODO: non è tanto carino passare gli ai_objects così....
        #preparing threads
        observer = Exercise_correcness_observer() #the object where I will store all the percentage of correctness returned by ai
	thread_legsx = Sensor_to_ai_thread(LEGSX_ADDRESS, SENSORPOSITION_LEGSX, aiLegsx, id_exercise, observer)
	thread_armsx = Sensor_to_ai_thread(LEGSX_ADDRESS, SENSORPOSITION_LEGSX, aiLegsx, id_exercise, observer)

	#threads will start when semaphore unloks
        semaphore = ts.Semaphore()
        thread_legsx.start(semaphore)
        thread_armsx.start(semaphore)

        cuntdown(START_CUNTDOWN)
        ts.semaphore.unlock()

        #contdown during the execution of the exercise
        cuntdown(seconds)

        #stopping two threads
        ts.semaphore.lock()
        thread_legsx.join()
        thread_armsx.join()

        #final report
        output_interface.output(observer.get_correctness_average())

def record_exercise(id_exercise, seconds):
	countdown(START_COUNTDOWN)
	thread_legsx = Thread(target = sf.record_sensor_data, args = (id_exercise, seconds, SENSORPOSITION_LEGSX, LEGSX_ADDRESS))
	thread_armsx = Thread(target = sf.record_sensor_data, args = (id_exercise, seconds, SENSORPOSITION_ARMSX, ARMSX_ADDRESS))
        thread_legsx.start()
        thread_armsx.start()
        ts.semaphore.unlock()
        thread_legsx.join()
        thread_armsx.join()
        ts.semaphore.lock()


def countdown(value):
	for x in reversed(xrange(1, value):
		oldnow = time.time
		vs.say(str(x))
		time.sleep(1.0 - (time.time() - oldnow))
	vs.say("go")


