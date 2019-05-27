#coding: utf-8

import _test_output as output_interface
import time



def start(initial_value):
	"""cuntdown from initial_value to 0. Each second I give output remaining seconds"""
  	for x in reversed(xrange(1, initial_value)):
		oldnow = time.time()
		output_interface.output(str(x))
		time.sleep(1.0 - (time.time() - oldnow))

#main
start(5)