#coding: utf-8

import main_functions as mf
import db_functions as db
import ai_functions as ai
import config

SENSORPOSITION_LEGSX	        = config.SENSORPOSITION_LEGSX
SENSORPOSITION_ARMSX	        = config.SENSORPOSITION_ARMSX

#REGISTRATION PHASE

#init
mf.init_vocal_synthesizer()

#esercizi e descrizioni vanno caricati su DB prima della registrazione
"""

EXERCISE_ID = 1
EXERCISE_NAME = "prova2"
EXERCISE_DESCRIPTION = "destra e sinistra con armsx"

db_exercises = db.Database()
table_exercises = db_exercises.table_exercises
if(not table_exercises.is_already_present(EXERCISE_ID)):
  print(table_exercises.add_new_exercise(EXERCISE_ID, EXERCISE_NAME, EXERCISE_DESCRIPTION))



while(True):
    mf.init_sensors()
    #new_exercise_id = mf.select_new_exercise_id()
    #seconds = mf.select_seconds()
    mf.record_exercise(1, 10)  


"""
#CORRECTION PHASE
#init
mf.AI_sensor_legsx = ai.TheBrain(SENSORPOSITION_LEGSX)
mf.AI_sensor_armsx = ai.TheBrain(SENSORPOSITION_ARMSX)
mf.AI_sensor_legsx.fit_from_csv()
mf.AI_sensor_armsx.fit_from_csv()
mf.AI_sensor_legsx.serialize()
mf.AI_sensor_armsx.serialize()

print("DEBUG:  ", mf.AI_sensor_armsx.rfc.classes_)
print("DEBUG:  ", mf.AI_sensor_legsx.rfc.classes_)


mf.init_ai()
while(True):
    mf.init_sensors()
    exercise = mf.select_exercise()
    #seconds = mf.select_seconds()
    mf.do_exercise(exercise, 10)


