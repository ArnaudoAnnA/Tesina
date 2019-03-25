# -*- coding: utf-8 -*-

#------------------------------------------------------
# versione Python 2
#------------------------------------------------------

#costanti
SECONDI_PRE_REGISTRAZIONE = 5


LETTERA_BOTTONE_SINISTRA = "S"
LETTERA_BOTTONE_CENTRALE = "C"
LETTERA_BOTTONE_DESTRA = "D"

TUTTO_SPENTO = 0
TIMER_IN_IMPOSTAZIONE = 1
TIMER_IMPOSTATO_REGISTRAZIONE_ESERCIZIO = 2
TEMPO_FINITO = -1

import FILE_AUDIO
import time
import audio_timer
import output_per_test as outputInterface


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


# ---- main ---------------------------------------------------------------------------------------------------------------------------

#la situazione inziale è "timer non impostato" e "esercizio non registrato"
statoTimer = TIMER_IN_IMPOSTAZIONE;
datasetEsercizio = [0]  #MOK
timerDaImpostare = audio_timer.Timer(0)

while(1):
    print("  premi:\n  -C per tasto centrale\n  -S per tasto sinistra\n  -D per tasto destra\n")
    lettera = str(raw_input()) # https://www.geeksforgeeks.org/taking-input-from-console-in-python/
    if (lettera == LETTERA_BOTTONE_SINISTRA):
        click_bottone_sinistra()
    elif (lettera == LETTERA_BOTTONE_CENTRALE):
        click_bottone_centrale()
    elif (lettera == LETTERA_BOTTONE_DESTRA):
        click_bottone_destra()





