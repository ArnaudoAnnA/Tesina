#coding: utf-8

import config
import pyttsx
import threading


VS_RATE         = config.VS_RATE
VS_VOICE        = config.VS_VOICE
VS_VOLUME       = config.VS_VOLUME


thread = None

def init():
        global thread
        thread = Vocal_syntesizer()
        thread.start()


def output(string):
        """function that outputs the string given by audio through the vocal synthesizer"""
        global thread
        if(thread == None) :
                init()
        
        thread.to_be_said = string      #text to speech start in a separate thread to avoid slowing 
        if(thread.engine.isBusy()):
                thread.engine.stop()

class Vocal_syntesizer(threading.Thread):

        def __init__(self):
                threading.Thread.__init__(self)
                self.engine = pyttsx.init()
                self.engine.setProperty('rate', VS_RATE)
                self.engine.setProperty('voice', VS_VOICE)
                self.engine.setProperty('volume', VS_VOLUME)
                self.to_be_said = None

        def run(self):
                """function that outputs the string given by audio through the vocal synthesizer"""
                while(True):
                        if(self.to_be_said != None):
                                self.engine.say(self.to_be_said)
                                self.to_be_said = None
                                self.engine.runAndWait()
