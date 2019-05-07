
# -*- coding: utf-8 -*-

import time
import audio_timer
import audio_raspberry as output_interface
import audio_files_ita as audio_files

TIME_BEFORE_START = 5
MINIMUM_CORRECTNESS_PERCENTAGE = 65

class AudioFeedbackExercise:
  
  correctness_sum = 0
  n_feedback = 0
  
  #function that manages the timer during the correction phase
  @staticmethod
  def outputTimer(seconds):
    AudioFeedbackExercise.medium_correctness = 0
    AudioFeedbackExercise.n_feedback = 0

    #initial countdown
    countdown = audio_timer.Timer(TIME_BEFORE_START)
    output_interface.audio_output(audio_files.DIRECTORY_PATH, [audio_files.REGISTRATION_WILL_START_IN, audio_files.NUMBERS[TIME_BEFORE_START], audio_files.SECONDS])
    countdown.audio_countdown(1)

    #acquisition and correction phase
    output_interface.audio_output(audio_files.DIRECTORY_PATH, audio_files.GO)
    time.sleep(1)
    timer = audio_timer.Timer(seconds)
    timer.audio_countdown(1)  
    
    #report exercise execution
    medium_correctness = AudioFeedbackExercise.medium_correctness / AudioFeedbackExercise.n_feedback
    output_interface.audio_output(audio_files.DIRECTORY_PATH, [audio_files.EXERCISE_DONE_WITH, audio_files.NUMBERS[medium_correctness], PERCENTAGE_OF_CORRECTNESS)

  #function called by thread every time the AI algorithm recognizes a movement class
  @staticmethod
  def movement_feedback_notify(sensor, correctness_percentage):

    if(correctnessPercentage < MINIMUM_CORRECTNESS_PERCENTAGE):
      output_interface.audio_output(faudio_files.DIRECTORY_PATH, [audio_files.SENSOR_ERROR, audio_files.SENSOR_POSITON[sensor]])
  
    #saving report
    AudioFeedbackExercise.correctness_sum += correctness_percentage
    AudioFeedbackExercise.n_feedback += 1
