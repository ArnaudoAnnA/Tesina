
# -*- coding: utf-8 -*-

import time
import audio_timer
import audio_raspberry as output_interface
import audio_files_ita as audio_files
import ia_functions
import thread_semaphore

TIME_BEFORE_START = 5
MINIMUM_CORRECTNESS_PERCENTAGE = 65

class Live_exercise_correction:
  
  correctness_sum = 0
  n_feedback = 0

#---------------------------------------------------------------------------------------------------------------  
  
  @staticmethod
  def do_exercise(id_exercise, seconds):
    #IA
    IA_sensorLegSx = ia_funcions.TheBrain(config.SENSORPOSITION_LEGSX)
    IA_sensorArmDx = ia_funcions.TheBrain(config.SENSORPOSITION_ARMDX)
    IA_sensorLegSx.unserialize()
    IA_sensorArmDx.unserialize()
    
    #semaphore for threads
    semaphore = thread_semaphore.Semaphore()
    
    #starting threads (IA threads will run only when the semaphore is unlocked)
    IA_sensorLegSx.start(id_exercise, semaphore)
    IA_sensorArmDx.start(id_exercise, semaphore)
    
    #the timer will unlock the semaphore when the initial cuntdown has finished
    Live_exercise_correction.outputTimer(seconds, semaphore)  
    
    #when the timer has finished the cuntdown from "seconds" to zero
    IA_sensorLegSx.join()
    IA_sensorArmDx.join()
    
    #report exercise execution
    medium_correctness = AudioFeedbackExercise.medium_correctness / AudioFeedbackExercise.n_feedback
    output_interface.audio_output(audio_files.DIRECTORY_PATH, [audio_files.EXERCISE_DONE_WITH, audio_files.NUMBERS[medium_correctness], PERCENTAGE_OF_CORRECTNESS)

#-----------------------------------------------------------------------------------------------------------------------------------   
  
  #function that manages the timer during the correction phase
  @staticmethod
  def outputTimer(seconds, semaphore):
    AudioFeedbackExercise.medium_correctness = 0
    AudioFeedbackExercise.n_feedback = 0

    #initial countdown
    countdown = audio_timer.Timer(TIME_BEFORE_START)
    output_interface.audio_output(audio_files.DIRECTORY_PATH, [audio_files.REGISTRATION_WILL_START_IN, audio_files.NUMBERS[TIME_BEFORE_START], audio_files.SECONDS])
    countdown.audio_countdown(1)
                                                               
    semaphore.unlock()                                                           

    #acquisition and correction phase
    output_interface.audio_output(audio_files.DIRECTORY_PATH, audio_files.GO)
    time.sleep(1)
    timer = audio_timer.Timer(seconds)
    
    semaphore.lock()                                                           
    
    
  #function called by thread every time the AI algorithm recognizes a movement class
  @staticmethod
  def ia_result_notify(sensor, correctness_percentage):

    if(correctnessPercentage < MINIMUM_CORRECTNESS_PERCENTAGE):
      output_interface.audio_output(faudio_files.DIRECTORY_PATH, [audio_files.SENSOR_ERROR, audio_files.SENSOR_POSITON[sensor]])
  
    #saving report
    AudioFeedbackExercise.correctness_sum += correctness_percentage
    AudioFeedbackExercise.n_feedback += 1
