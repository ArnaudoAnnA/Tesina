#coding: utf-8



import vocal_synthesizer as output_interface
import time



def start(initial_value):
	"""cuntdown from initial_value to 0. Each second I give output remaining seconds"""
  	for x in reversed(xrange(1, initial_value)):
		oldnow = time.time()
		output_interface.output(str(x))
		delay = float(time.time()) - oldnow
		time.sleep(1.0 - delay)
