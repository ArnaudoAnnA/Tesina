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
HOME_PATH=config.HOME_PATH

DIRECTORY_PATH = HOME_PATH+"files/wav/"

#timer
VALORE_SCARTATO = "valore scartato"
ISTRUZIONI_IMPOSTAZIONE_TIMER = "istruzioni_impostazione_timer.wav"
CONFERMARE_NUMERO = "Vuoi confermare il numero selezionato? Destra per si, sinistra per no"
REGISTRAZIONE_AVVIATA_TRA = "la registrazione sarà avviata tra {} secondi"
VIA = "via"
REGISTRAZIONE_TERMINATA = "registrazione terminata"

NUMERI = ["zero.mp3", "uno.wav", "due.wav", "tre.wav", "quattro.wav", "cinque.wav"]

#exercise feedback
ERRORE_SENSORE = "errore sensore {}" #sostituire, in seguito, al numero del sensore la sua posizione
PERCENTUALE_CORRETTEZZA = "esercizio eseguito con {} per cento di correttezza" 

#exercise selection
NESSUN_ESERCIZIO_DISPONIBILE = "nessun esercizio disponibile"
USARE_FRECCE_PER_SELEZIONARE_ESERCIZIO = "usare le frecce per selezionare l'esercizio"
ESERCIZIO = "esercizio"
