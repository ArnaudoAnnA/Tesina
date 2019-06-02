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
    "CONFIRM" : "Vuoi confermare l'elemento selezionato? Destra per si, sinistra per no",

    #setting timer
    "TIMER_SETTINGS_BEGIN" : "Specificare il numero di secondi di durata dell'esercizio. premere sul tasto centrale per iniziare",
    # dizionario che associa un id progressivo con il numero di secondi in cui l'esercizio verrà eseguito (sia in valore numerico che in stringa)
    "TIME_DICTIONARY" :	{
      10: "10 secondi",
      30: "30 secondi",
      60: "60 secondi",
      120: "120 secondi",
      180: "180 secondi" ,
      240: "240 secondi",
      300: "300 secondi",
      360: "360 secondi" ,
      420: "420 secondi",
      480: "480 secondi",
      540: "540 secondi",
      600: "600 secondi"
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
    "SELECT_THE_EXERCISE" : "usare le frecce per selezionare l'esercizio",


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
