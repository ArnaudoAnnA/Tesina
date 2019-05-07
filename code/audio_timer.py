# -*- coding: utf-8 -*-

#------------------------------------------------------
#Python 2



#AUDIO_TIMER
#this module implements a timer with an audio interface
#------------------------------------------------------
import time
import audio_file_ita as audio
import audio_raspberry as audio_interface

#constants
DIRECTORY_PATH = FILE_AUDIO.DIRECTORY_PATH
NUMS = FILE_AUDIO.NUMS

TIME_OUT = -1

class Timer:
    timer = 0

    def __init__(self, initial_value):
        self.timer = initialValue


    def setTimer(self, new):
        self.timer = new
        return TimerChangedListener.notify(self.timer)

    # --------------------------------------------------------------------------------------------------------------------------------------
    def increaseTimer(self, increment):
		self.timer = self.timer + increment
		return TimerChangedListener.notify(self.timer)
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
        audio_interface.audio_output([DIRECTORY_PATH + NUMBERS[timer]])
        if (timer == 0):
            return TIME_OUT
