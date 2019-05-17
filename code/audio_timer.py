# -*- coding: utf-8 -*-

#------------------------------------------------------
#Python 2



#AUDIO_TIMER
#this module implements a timer with an audio interface
#------------------------------------------------------
import time
import audio_files_ita as audio_files
import raspberry_output as audio_interface

#constants
DIRECTORY_PATH = audio_files.DIRECTORY_PATH
NUMBERS = audio_files.NUMBERS

TIME_OUT = -1

class Timer:

    def __init__(self, initial_value):
        self.value = initial_value


    def set(self, new):
        self.value = new
        return TimerChangedListener.notify(self.value)

    # --------------------------------------------------------------------------------------------------------------------------------------
    def increase(self, increment):
        self.value = self.value + increment
        return TimerChangedListener.notify(self.value)
    #------------------------------------------------------------------------------------------------------------------------------------
    def audio_countdown(self, lapse):
        while self.increaseTimer(-lapse) != TIME_OUT:
            time.sleep(lapse)  # wait 

    # --------------------------------------------------------------------------------------------------------------------------------------------------




# --------------------------------------------------------------------------------------------------------------------------------------------------

class TimerChangedListener:

    @staticmethod
    def notify(timer):
    	#called every time the timer changes value, returns the new timer value: if it's 0, returns TIME_OUT
        audio_interface.output(DIRECTORY_PATH , [NUMBERS[timer]])
        if (timer == 0):
            return TIME_OUT
            
            