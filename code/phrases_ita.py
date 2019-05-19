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
DISCARDED_VALUE = "valore scartato"
NUMBER_SETTINGS_GUIDE = "per aumentare il numero premi il bottone destra, per diminuire quello di sinistra"
CONFIRM = "Vuoi confermare il numero selezionato? Destra per si, sinistra per no"

#setting timer
TIMER_SETTINGS_BEGIN = "Specificare il numero di secondi di durata dell'esercizio. premere sul tasto centrale per iniziare"
# dictionary that associates a progressive id with the number of seconds the exercise will be executed (in both numerical and string value)
"""DA TRADURRE IN ITALIANO"""
time_dictionary =	{
  10: "ten seconds",
  30: "thirty seconds",
  60: "one minute",
  120: "two minutes",
  180: "three minutes" ,
  240: "four minutes",
  300: "five minutes",
  360: "six minutes" ,
  420: "seven minutes",
  480: "eight minutes",
  540: "nine minutes",
  600: "ten minutes"
}

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
