# -*- coding: utf-8 -*-

import pyttsx
import vocal_synthesizer as vs

#test = vs.Vocal_synthesizer()
#test.say("funziona")

engine = pyttsx.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('rate', 'default')

engine.setProperty('voice', 'en-scottish')


engine.say('Registration will start in 5 seconds')

"""
for voice in voices:
   engine.setProperty('voice', voice.id)
   print(voice.id)
   engine.say(voice.id+'. Per aumentare premere il bottone destra, per diminuire quello di sinistra.')
"""
engine.runAndWait()
