#coding: utf-8

import main_functions as mf
import config

SENSORPOSITION_LEGSX	        = config.SENSORPOSITION_LEGSX
SENSORPOSITION_ARMSX	        = config.SENSORPOSITION_ARMSX

#REGISTRATION PHASE

#init
mf.init_vocal_synthesizer()
mf.init_sensors()
ai_lsx = mf.new_ai(SENSORPOSITION_LEGSX)
ai_asx = mf.new_ai(SENSORPOSITION_ARMSX)

#esercizi e descrizioni vanno caricati su DB prima della registrazione

while(True):
    new_exercise_id = mf.select_exercise_to_record()
    seconds = mf.select_seconds()
    mf.record_exercise(new_exercise_id, seconds)
    ai_lsx.save_fit_ai()
    ai_asx.save_fit_ai()
    

