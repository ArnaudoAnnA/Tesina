# -*- coding: utf-8 -*-
#  Python 2
#  ITALIAN VERSION
#-----------------------------------------------------------------------
#  la lista costante contiene l'elenco dei file .wav
# 
#  ALERT: tutti i vale devono essere .wav 
#         tutti i file devono avere il path assoluto
#-----------------------------------------------------------------------

import config

dictionary = {

    #setting number
    "DISCARDED_VALUE" : "valore scartato",
    "NUMBER_SETTINGS_GUIDE" : "per selezionare gli elementi seguenti premere il tasto destro, per i percedenti premere il tasto sinistro",
    "CONFIRM" : "Vuoi confermare il numero selezionato? Destra per si, sinistra per no",

    #setting timer
    "TIMER_SETTINGS_BEGIN" : "Specificare il numero di secondi di durata dell'esercizio. premere sul tasto centrale per iniziare",
    # dizionario che associa un id progressivo con il numero di secondi in cui l'esercizio verrà eseguito (sia in valore numerico che in stringa)
    "time_dictionary" :	{
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
    },

    #registration
    "ID_EXERCISE_SETTINGS_BEGIN" : "Specificare l'id del nuovo esercizio. premere sul tasto centrale per iniziare",
    "SENDING_DATA" : "invio dati in corso",
    "REGISTRATION_WILL_START_IN" : "la registrazione sarà avviata tra",
    "REGISTRATION_ENDED" : "registrazione terminata",

    #feedback 
    "ERROR_FEEDBACK" : "errore sensore", #sostituire, in seguito, al numero del sensore la sua posizione
    "EXERCISE_DONE_WITH" : "esercizio eseguito con",
    "PERCENTAGE_OF_CORRECTNESS" : "per cento di correttezza",

    #exercise selection
    "NO_AVAIABLE_EXERCISE" : "nessun esercizio disponibile",
    "USE_THE_ARROWS_TO_SELECT_THE_EXERCISE" : "usare le frecce per selezionare l'esercizio",


    #generals
    "SECONDS" : "secondi",
    "GO" : "via",
    "SENSOR_POSITION" : {
          config.SENSORPOSITION_LEGSX : "gamba sinistra",
          config.SENSORPOSITION_LEGDX : "gamba destra",
          config.SENSORPOSITION_ARMSX : "braccio sinistro",
          config.SENSORPOSITION_ARMDX : "braccio destro",
        }
}
