#coding: utf-8



import vocal_synthesizer as output_interface
import time



def start(initial_value):
	"""cuntdown from initial_value to 0. Each second I give output remaining seconds"""
  	for x in range(initial_value, 0, -1):
		oldnow = time.time()
		output_interface.output(str(x), 250)
		delay = float(time.time()) - oldnow
		if (delay >= 0.0 and delay < 1.0) :
                        time.sleep(1.0 - delay)
