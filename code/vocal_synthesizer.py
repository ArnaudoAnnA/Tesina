import pyttsx
import config

VS_RATE         = config.VS_RATE
VS_VOICE        = config.VS_VOICE
VS_VOLUME       = config.VS_VOLUME


engine = None

def init():
        engine = pyttsx.init()
        engine.setProperty('rate', VS_RATE)
        engine.setProperty('voice', VS_ID)
        engine.setProperty('volume', VS_VOLUME)


def output(self, string):
        """function that outputs the string given by audio through the vocal synthesizer"""
        engine.say(string)
        engine.runAndWait()

