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

DIRECTORY_PATH = config.HOME_PATH + "file/audio/"

#setting number
DISCARDED_VALUE = "valore scartato"
NUMBER_SETTINGS_GUIDE = "per aumentare il numero premi il bottone destra, per diminuire quello di sinistra"
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
NUMBERS = ["zero.mp3", "uno.wav", "due.wav", "tre.wav", "quattro.wav", "cinque.wav"]
SECONDS = "secondi"
GO = "via"
SENSOR_POSITION = {
      config.SENSORPOSITION_LEGSX : "legsx",
      config.SENSORPOSITION_LEGDX : "legdx",
      config.SENSORPOSITION_ARMSX : "armsx",
      config.SENSORPOSITION_ARMDX : "armdx",
    }