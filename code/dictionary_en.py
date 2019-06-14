# -*- coding: utf-8 -*-
#  Python 2
#  ENGLISH VERSION
#-----------------------------------------------------------------------
#  constant list containing .wav file list
# 
#  ALERT: every file must be .wav 
#         every file must have absolute path
#-----------------------------------------------------------------------

import config

dictionary = {

    #setting number
    "DISCARDED_VALUE" : "value discarded",
    "NUMBER_SETTINGS_GUIDE" : "use right or left arrow to go forward or back",
    "CONFIRM" : "Do you want confirm",

    #setting timer
    "TIMER_SETTINGS_BEGIN" : "how long do you want to exercise?",
    # dictionary that associates a progressive id with the number of seconds the exercise will be executed (in both numerical and string value)
    "TIME_DICTIONARY" :	{
      0 : "zero seconds",
      10: "ten seconds",
      30: "thirty seconds",
      60: "one minute",
      120: "two minutes",
      180: "three minutes" ,
      240: "four minutes",
      300: "five minutes",
      360: "six minutes" ,
      420: "seven minutes",
      480: "eight minutes",
      540: "nine minutes",
      600: "ten minutes"
    },

    #registration
    "ID_EXERCISE_SETTINGS_BEGIN" : "Specify id of the new exercise.",
    "SENDING_DATA" : "Sending data in progress",
    "REGISTRATION_WILL_START_IN" : "The registration will start in",
    "REGISTRATION_ENDED" : "end registration",

    #feedback 
    "ERROR_FEEDBACK" : "error", #replace, then the number of the senosor, its position
    "CORRECT" : "correct",
    "EXERCISE_DONE_WITH" : "exercise done with ",
    "PERCENTAGE_OF_CORRECTNESS" : " percentage of correctness",
    
    #exercise selection
    "NO_AVAIABLE_EXERCISE" : "no exercises available",
    "SELECT_THE_EXERCISE" : "use the pushbutton to select the exercise",


    #generals
    "YES" : "yes",
    "NO" : "no",
    "SECONDS" : "seconds",
    "GO" : "go",
    #sensor positions
    config.SENSORPOSITION_LEGSX : "left leg",
    config.SENSORPOSITION_LEGDX : "right leg",
    config.SENSORPOSITION_ARMSX : "left arm",
    config.SENSORPOSITION_ARMDX : "right arm"
}
