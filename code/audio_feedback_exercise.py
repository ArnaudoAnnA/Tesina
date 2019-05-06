
# -*- coding: utf-8 -*-

import time
import audio_timer
import audio_raspberry as output_interface
import audio_file_ita as audio

REGISTRATION_COMMENCES_IN_SECONDS = audio.REGISTRATION_COMMENCES_IN_SECONDS
EXERCISE_REPORT = audio.EXERCISE_REPORT
ERROR_FEEDBACK = audio.ERROR_FEEDBACK
GO = audio.GO

CORRECTION_TIME_SPAN = 5
MINIMUM_CORRECTNESS_PERCENTAGE = 65

class AudioFeedbackExercise:
  
  correctness_sum = 0
  n_feedback = 0
  #function that manages the timer during the correction phase
  @staticmethod
  def outputTimer(time):
    AudioFeedbackExercise.medium_correctness = 0
    AudioFeedbackExercise.n_feedback = 0
    timer = audio_timer.Timer(time)

    #initial countdown
    countdown = audio_timer.Timer(CORRECTION_TIME_SPAN)
    output_interface.audio_output(REGISTRATION_COMMENCES_IN_SECONDS.format(REGISTRATION_TIME_SPAN))
    countdown.audio_countdown(1)

    #acquisition and correction phase
    output_interface.audio_output(GO)
    time.sleep(1)
    timer.audio_countdown(1)  
    
    #report exercise execution
    medium_correctness = AudioFeedbackExercise.medium_correctness / AudioFeedbackExercise.n_feedback
    output_interface.audio_output(EXERCISE_REPORT.format(medium_correctness))

  #function called by thread every time the AI algorithm recognizes a movement class
  @staticmethod
  def movement_feedback_notify(sensor, correctness_percentage):

    if(correctnessPercentage < MINIMUM_CORRECTNESS_PERCENTAGE):
      output_interface.audio_output(ERROR_FEEDBACK.format(sensor))
  
    #saving report
    AudioFeedbackExercise.correctness_sum += correctness_percentage
    AudioFeedbackExercise.n_feedback += 1
