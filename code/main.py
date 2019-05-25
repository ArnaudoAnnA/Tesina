#coding: utf-8

import main_functions as mf
import db_functions ad db

#REGISTRATION PHASE

#init
mf.init_sensor_vocal_synthesizer()

#esercizi e descrizioni vanno caricati su DB prima della registrazione
"""
db_exercises = db.Database()
table_exercises = db_exercises.table_exercises
if(!table_exercises.id_already_present(EXERCISE_ID)):
  table_exercises.add_new_exercise(EXERCISE_ID, EXERCISE_NAME, EXERCISE_DESCRIPTION)
"""
While(True):
    new_exercise_id = mf.select_new_exercise_id()
    seconds = mf.select_seconds()
    mf.record_exercise(new_exercise_id, seconds)  


#CORRECTION PHASE
#init
mf.init_sensor_vocal_synthesizer()
mf.init_AI()

while(True):
    exercise = mf.select_exercise()
    seconds = mf.select_seconds()
    mf.do_exercise(exercise, seconds)
