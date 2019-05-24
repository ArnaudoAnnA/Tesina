# -*- coding: utf-8 -*-
#  Python 2
#  ITALIAN VERSION
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
    "NUMBER_SETTINGS_GUIDE" : "to select following element press right button or press left button to select previous",
    "CONFIRM" : "Do you want confirm the selected number? Yes: Right, No: Left",

    #setting timer
    "TIMER_SETTINGS_BEGIN" : "Specify the number of sensonds about the duration of the exercise. Click the central botton to start",
    # dictionary that associates a progressive id with the number of seconds the exercise will be executed (in both numerical and string value)
    "time_dictionary" :	{
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
    "ID_EXERCISE_SETTINGS_BEGIN" : "Specify id of the new exercise. Click the central botton to start",
    "SENDING_DATA" : "Sending data in progress...",
    "REGISTRATION_WILL_START_IN" : "The registration will be sent after...",
    "REGISTRATION_ENDED" : "end registration",

    #feedback 
    "ERROR_FEEDBACK" : "errore", #replace, then the number of the senosor, its position
    "EXERCISE_DONE_WITH" : "exercise executed with {} per cent of correctness",

    #exercise selection
    "NO_AVAIABLE_EXERCISE" : "no exercises available",
    "USE_THE_ARROWS_TO_SELECT_THE_EXERCISE" : "use arrows to select the exercise",


    #generals
    "SECONDS" : "secondi",
    "GO" : "via",
    "SENSOR_POSITION" : {
          config.SENSORPOSITION_LEGSX : "left leg",
          config.SENSORPOSITION_LEGDX : "right leg",
          config.SENSORPOSITION_ARMSX : "left arm",
          config.SENSORPOSITION_ARMDX : "right arm",
        }
}
