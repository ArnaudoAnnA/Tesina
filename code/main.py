#coding: utf-8

import main_functions as mf
import db_functions ad db

EXERCISE_ID = 0
SECONDS = 0
#init
mf.init_sensor_vocal_synthesizer()

#REGISTRATION PHASE
EXERCISE_NAME = ""
EXERCISE_DESCRIPTION = ""


db_exercises = db.Database()
table_exercises = db_exercises.table_exercises
if(!table_exercises.id_already_present(EXERCISE_ID)):
  table_exercises.add_new_exercise(EXERCISE_ID, EXERCISE_NAME, EXERCISE_DESCRIPTION)
 
mf.record_exercise(EXERCISE_ID, SECONDS)  


#CORRECTION PHASE
mf.init_AI()
selected_exercise = mf.
