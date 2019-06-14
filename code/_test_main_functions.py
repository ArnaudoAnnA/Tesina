#coding: utf-8

import main_functions as mf
import time
import sys
import db_functions as db

print(time.time())
sys.stdout.flush()

mf.init_sensor_vocal_synthesizer()


"""
exercise = mf.select_exercise()
print(exercise)"""

"""
new_id = mf.select_new_exercise_id()
print(new_id)"""

"""
seconds = mf.select_seconds()
print(seconds)"""


#mf.record_exercise(11, 10)


mf.init_ai()
print("inizio addestramento...")
mf.AI_sensor_legsx.fit_from_csv()
print("fine addestramento")
mf.do_exercise(10, 10)


