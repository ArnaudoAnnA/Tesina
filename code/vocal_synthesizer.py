#coding: utf-8

import config
import pyttsx
import threading


VS_RATE         = config.VS_RATE
VS_VOICE        = config.VS_VOICE
VS_VOLUME       = config.VS_VOLUME


object = None
to_be_read = None

def init():
        global object
        object = Vocal_syntesizer()


def output(string):
        """function that outputs the string given by audio through the vocal synthesizer"""
        global object
        global to_be_read
        if(object == None) :
                init()
        to_be_read = string
        object.start()          #text to speech start in a separate thread to avoid slowing 


class Vocal_syntesizer(threading.Thread):

        def __init__(self):
                threading.Thread.__init__(self)
                self.engine = pyttsx.init()
                self.engine.setProperty('rate', VS_RATE)
                self.engine.setProperty('voice', VS_VOICE)
                self.engine.setProperty('volume', VS_VOLUME)

        def run(self):
                """function that outputs the string given by audio through the vocal synthesizer"""
                global to_be_read
                self.engine.say(to_be_read)
                self.engine.runAndWait()        
                #thread ends when the last instruction of this method is executed
