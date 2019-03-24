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

import time
import os  # utilizzo del modulo os: https://docs.python.org/2/library/os.html
        # in alternativa si può usare https://docs.python.org/2/library/pty.html#module-pty
        # la situazione inziale è "timer non impostato" e "esercizio non registrato"
import FILE_AUDIO




statoTimer = TUTTO_SPENTO;
timer = 0
datasetEsercizio = [0]  # MOCK


# --------------------------------------------------------------------------------------------------------------------------------------------------

def click_bottone_sinistra():
    global statoTimer
    global timer
    if (statoTimer == TIMER_IN_IMPOSTAZIONE):
        if (timer != 0):
            timer -= 1
            Timer_changed_listener.notify(timer)  # funzione che si occuperà di dare in output tramite interfaccia audio il nuovo valore del timer

    elif (statoTimer == TIMER_IMPOSTATO_REGISTRAZIONE_ESERCIZIO):  # l'utente decide di scartare l'esercizio appena registrato
        output_audio(FILE_AUDIO.VALORE_SCARTATO)
        datasetEsercizio = [0]
        timer = 0
        statoTimer = TUTTO_SPENTO

# --------------------------------------------------------------------------------------------------------------------------------------------------

def click_bottone_centrale():
    global statoTimer
    global timer
    if ( statoTimer == TUTTO_SPENTO):  # timer da impostare da capo (questo è il primo click sul tasto centrale)
        output_audio(FILE_AUDIO.SPIEGAZIONI_IMPOSTAZIONE_TIMER)
        statoTimer += 1

    elif (statoTimer == TIMER_IN_IMPOSTAZIONE and timer != 0):  # l'utente ha terminato l'impostazione del timer
        output_audio(FILE_AUDIO.CONFERMA_TIMER)
        statoTimer = TIMER_IMPOSTATO_REGISTRAZIONE_ESERCIZIO


# --------------------------------------------------------------------------------------------------------------------------------------------------

def click_bottone_destra():
    global statoTimer
    global timer
    if (statoTimer == TIMER_IN_IMPOSTAZIONE):
        timer+= 1
        Timer_changed_listener.notify(timer)

    elif (statoTimer == TIMER_IMPOSTATO_REGISTRAZIONE_ESERCIZIO) : # l'utente decide di mantenere l'esercizio appena registrato
        output_audio(FILE_AUDIO.INVIO_DATI_IN_CORSO)
        registra_esercizio()
        statoTimer = TUTTO_SPENTO


# --------------------------------------------------------------------------------------------------------------------------------------------------

class Timer_changed_listener:

    @staticmethod
    def notify(timer):  # metodo statico.
        # viene evocato ogni volta che il numero del timer cambia
        # da in output il nuovo valore del timer.
        # se il nuovo valore è 0, restituisce TEMPO_FINITO, che può essere ignorato o meno a seconda di dove viene richiamato il metodo
        output_audio(timer)
        if (timer == 0):
            return TEMPO_FINITO


# --------------------------------------------------------------------------------------------------------------------------------------------------
# thread che, contemporaneamente a quello che memorizza l'esercizio, scandisce il tempo

def registra_esercizio():
    global timer
    output_audio(FILE_AUDIO.INIZIO_REGISTRAZIONE_TRA_QUALCHE_SECONDO.format(SECONDI_PRE_REGISTRAZIONE))

    for n in range(SECONDI_PRE_REGISTRAZIONE, 0, -1):
        time.sleep(1)
        output_audio(n)


    output_audio(FILE_AUDIO.VIA)
    time.sleep(1)

    while Timer_changed_listener.notify(timer) != TEMPO_FINITO:
        timer -= 1
        time.sleep(1)  # aspetto un secondo

    output_audio(FILE_AUDIO.REGISTRAZIONE_TERMINATA)


# --------------------------------------------------------------------------------------------------------------------------------------------------
# gestire interfaccia audio di Raspberry: https://www.raspberrypi.org/documentation/usage/audio/README.mdaa
# utilizzo del modulo os: https://docs.python.org/2/library/os.html
def output_audio(messaggio):
   print(messaggio)

# ---- main ---------------------------------------------------------------------------------------------------------------------------



while(1):
    print("  premi:\n  -C per tasto centrale\n  -S per tasto sinistra\n  -D per tasto destra\n")
    lettera = str(raw_input()) # https://www.geeksforgeeks.org/taking-input-from-console-in-python/
    if (lettera == LETTERA_BOTTONE_SINISTRA):
        click_bottone_sinistra()
    elif (lettera == LETTERA_BOTTONE_CENTRALE):
        click_bottone_centrale()
    elif (lettera == LETTERA_BOTTONE_DESTRA):
        click_bottone_destra()





