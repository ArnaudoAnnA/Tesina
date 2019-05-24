#coding: utf-8

import vocal_synthesizer as vs
import time

def countdown(value):
  for x in reversed(xrange(1, value):
		oldnow = time.time
		vs.say(str(x))
		time.sleep(1.0 - (time.time() - oldnow))
