#coding: utf-8

import config
import pyttsx
import time
import threading
import thread_semaphore as ts
from Queue import Queue


VS_RATE         = config.VS_RATE
VS_VOICE        = config.VS_VOICE
VS_VOLUME       = config.VS_VOLUME

def init():
        global thread
        global thread_semaphore
        global to_say
        global rate
        to_say = Queue()
        rate = Queue()
        thread_semaphore = ts.Semaphore()
        thread = Vocal_syntesizer()
        thread.start()


def output(string, vs_rate = VS_RATE):
        """function that outputs the string given by audio through the vocal synthesizer"""
        to_say.put(string)      #text to speech start in a separate thread to avoid slowing 
        rate.put(vs_rate)
        thread_semaphore.unlock()
        print string


class Vocal_syntesizer(threading.Thread):

        def __init__(self):
                threading.Thread.__init__(self)

        def run(self):
                """function that outputs the string given by audio through the vocal synthesizer"""
                while(True):
                        thread_semaphore.wait_for_unlock()
                        thread_semaphore.lock()
                        while(not to_say.empty()):
                                out = str(to_say.get())
                                vs_rate = int(rate.get())
                                countdown = len(out)*1.0/((VS_RATE*5.0)/60.0) #time needed to say out
                                engine = _Vocal_engine(out, vs_rate)
                                engine.start()
                                engine.join(countdown + 2.0)
                                del(engine)


class _Vocal_engine(threading.Thread):

        def __init__(self, string, vs_rate):
                threading.Thread.__init__(self)
                self.engine = pyttsx.init()
                self.engine.setProperty('rate', vs_rate)
                self.engine.setProperty('voice', VS_VOICE)
                self.engine.setProperty('volume', VS_VOLUME)
                self.string = string

        def run(self):
                #print str(self) + "run"
                self.engine.say(self.string)
                self.engine.runAndWait()
                #print str(self) + "run finished"


                        

                
                
                
