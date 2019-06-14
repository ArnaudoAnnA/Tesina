#coding: utf-8

import main_functions as mf
import config

SENSORPOSITION_LEGSX	        = config.SENSORPOSITION_LEGSX
SENSORPOSITION_ARMSX	        = config.SENSORPOSITION_ARMSX


#CORRECTION PHASE
#init
mf.init_vocal_synthesizer()
mf.init_sensors()
ai_lsx = mf.init_ai(SENSORPOSITION_LEGSX)
ai_asx = mf.init_ai(SENSORPOSITION_ARMSX)

while(True):
    exercise = mf.select_exercise_to_do()
    seconds = mf.select_seconds()
    mf.do_exercise(exercise, seconds, ai_lsx, ai_asx)


