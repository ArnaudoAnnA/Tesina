# -*- coding: utf-8 -*-
#  Python 2
#  ITALIAN VERSION
#-----------------------------------------------------------------------
#  constant list containing .wav file list
# 
#  ALERT: every file must be .wav 
#         every file must have absolute path
#-----------------------------------------------------------------------

import config


#setting number
DISCARDED_VALUE = "value discarded"
NUMBER_SETTINGS_GUIDE = "to select following element press right button or press left button to select previous"
CONFIRM = "Vuoi confermare il numero selezionato? Destra per si, sinistra per no"

#setting timer
TIMER_SETTINGS_BEGIN = "Specificare il numero di secondi di durata dell'esercizio. premere sul tasto centrale per iniziare"

#registration
ID_EXERCISE_SETTINGS_BEGIN = "Specificare l'id del nuovo esercizio. premere sul tasto centrale per iniziare"
SENDING_DATA = "invio dati in corso"
REGISTRATION_WILL_START_IN = "la registrazione sarà avviata tra"
REGISTRATION_ENDED = "registrazione terminata"

#feedback 
ERROR_FEEDBACK = "errore sensore" #sostituire, in seguito, al numero del sensore la sua posizione
EXERCISE_DONE_WITH = "esercizio eseguito con"
PERCENTAGE_OF_CORRECTNESS = "per cento di correttezza"

#exercise selection
NO_AVAIABLE_EXERCISE = "nessun esercizio disponibile"
USE_THE_ARROWS_TO_SELECT_THE_EXERCISE = "usare le frecce per selezionare l'esercizio"


#generals
SECONDS = "secondi"
GO = "via"
SENSOR_POSITION = {
      config.SENSORPOSITION_LEGSX : "gamba sinistra",
      config.SENSORPOSITION_LEGDX : "gamba destra",
      config.SENSORPOSITION_ARMSX : "braccio sinistro",
      config.SENSORPOSITION_ARMDX : "braccio destro",
    }
