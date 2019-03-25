# -*- coding: utf-8 -*-

#------------------------------------------------------
# versione Python 2

#IMPOSTA_TIMER_PER_REGISTRAZIONE
#si occupa della parte di impostazione del timer prima della registrazione dell'esercizio.

#IMPORTANTE: richiede che sul raspberry sia installata la libreria Rpy.GPIO
#------------------------------------------------------

#costanti

PIN_BOTTONE_SINISTRA = 3
PIN_BOTTONE_CENTRALE = 4
PIN_BOTTONE_DESTRA = 5

TUTTO_SPENTO = 0
TIMER_IN_IMPOSTAZIONE = 1
TIMER_IMPOSTATO_REGISTRAZIONE_ESERCIZIO = 2

SECONDI_PRE_REGISTRAZIONE = 5

import FILE_AUDIO
import RPi.GPIO as GPIO
import time
import audio_timer
import raspberry_audio as outputInterface


def click_bottone_sinistra():
    global statoTimer
    global timer
    if (statoTimer == TIMER_IN_IMPOSTAZIONE):
        if (timerDaImpostare.timer != 0):
            timerDaImpostare.incrementaTimer(-1)

    elif (statoTimer == TIMER_IMPOSTATO_REGISTRAZIONE_ESERCIZIO):  # l'utente decide di scartare l'esercizio appena registrato
        outputInterface.output_audio(FILE_AUDIO.VALORE_SCARTATO)
        datasetEsercizio = [0]  #non è il caso di azzerare anche il timer perchè alla prossima pressione del tasto centrale verrà istanziato un nuovo oggetto timer
        statoTimer = TUTTO_SPENTO

# --------------------------------------------------------------------------------------------------------------------------------------------------

def click_bottone_centrale():
    global statoTimer
    global timerDaImpostare

    if ( statoTimer == TUTTO_SPENTO):  # timer da impostare da capo (questo è il primo click sul tasto centrale)
        outputInterface.output_audio(FILE_AUDIO.SPIEGAZIONI_IMPOSTAZIONE_TIMER)
        statoTimer = TIMER_IN_IMPOSTAZIONE
        timerDaImpostare = audio_timer.Timer(0)  #istazio un nuovo oggetto timer

    elif (statoTimer == TIMER_IN_IMPOSTAZIONE and timerDaImpostare.timer != 0):  # l'utente ha terminato l'impostazione del timer
        outputInterface.output_audio(FILE_AUDIO.CONFERMA_TIMER)
        statoTimer = TIMER_IMPOSTATO_REGISTRAZIONE_ESERCIZIO


# --------------------------------------------------------------------------------------------------------------------------------------------------

def click_bottone_destra():
    global statoTimer
    global timer
    if (statoTimer == TIMER_IN_IMPOSTAZIONE):
        timerDaImpostare.incrementaTimer(+1)

    elif (statoTimer == TIMER_IMPOSTATO_REGISTRAZIONE_ESERCIZIO) : # l'utente decide di mantenere l'esercizio appena registrato
        outputInterface.output_audio(FILE_AUDIO.INVIO_DATI_IN_CORSO)
        audio_acquisizione_esercizio()
        statoTimer = TUTTO_SPENTO

# --------------------------------------------------------------------------------------------------------------------------------------------------
# thread che, contemporaneamente a quello che memorizza l'esercizio, scandisce il tempo

def audio_acquisizione_esercizio():
    global timer

    outputInterface.output_audio(FILE_AUDIO.INIZIO_REGISTRAZIONE_TRA_QUALCHE_SECONDO.format(SECONDI_PRE_REGISTRAZIONE))

    conto_alla_rovescia_pre_registrazione = audio_timer.Timer(SECONDI_PRE_REGISTRAZIONE)
    conto_alla_rovescia_pre_registrazione.audio_conto_alla_rovescia()                                   #"5..4..3..2.."

    outputInterface.output_audio(FILE_AUDIO.VIA)                                                        #"via"
    time.sleep(1)

    timerDaImpostare.audio_conto_alla_rovescia()                                                        #"7..6..5..4.."

    outputInterface.output_audio(FILE_AUDIO.REGISTRAZIONE_TERMINATA)                                    #"registrazione terminata"


# ------- MAIN ----------------------------------------------------------------------------------------------------

GPIO.setmode(GPIO.BCM) 								#specifico quale configurazione di pin intendo usare
GPIO.setup(PIN_BOTTONE_SINISTRA, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #PUD_DOWN significa che, se non viene ricevuto nessun segnale da raspberry, l'input del pin è di default 0
													#questa istruzione è importante per evitare errori dovuti a variazioni di tensione, che avvengono anche quando un pin non riceve voltaggio, per motivi fisici 
GPIO.setup(PIN_BOTTONE_CENTRALE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(PIN_BOTTONE_DESTRA, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#la situazione inziale è "timer non impostato" e "esercizio non registrato"
statoTimer = TIMER_IN_IMPOSTAZIONE;
datasetEsercizio = [0]  #MOK
timerDaImpostare = audio_timer.Timer(0)

#aggiungo un event_detect ad ogni pin e associo la relativa funzione che gestirà l'evento click sul bottone
#ulteriori spiegazioni:  https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
#SINISTRA
GPIO.add_event_detect(PIN_BOTTONE_SINISTRA, GPIO.FALLING) 	#GPIO.FALLING significa che l'evento si scatena nel momento in cui il bottone viene premuto (non quando viene rilasciato)

GPIO.add_event_callback(PIN_BOTTONE_SINISTRA, click_bottone_sinistra)


#CENTRO
GPIO.add_event_detect(PIN_BOTTONE_CENTRALE, GPIO.FALLING)
GPIO.add_event_callback(PIN_BOTTONE_CENTRALE, click_bottone_centrale)

#DESTRA
GPIO.add_event_detect(PIN_BOTTONE_DESTRA, GPIO.FALLING)
GPIO.add_event_callback(PIN_BOTTONE_DESTRA, click_bottone_destra)



