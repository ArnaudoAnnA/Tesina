#coding: utf-8

import config
import pyttsx


VS_RATE         = config.VS_RATE
VS_VOICE        = config.VS_VOICE
VS_VOLUME       = config.VS_VOLUME


engine = None

def init():
        global engine
        engine = pyttsx.init()
        engine.setProperty('rate', VS_RATE)
        engine.setProperty('voice', VS_VOICE)
        engine.setProperty('volume', VS_VOLUME)


def output(string):
        """function that outputs the string given by audio through the vocal synthesizer"""
        global engine
        if(engine == None) :
                init()
                
        engine.say(string)
        engine.runAndWait()

