# -*- coding: utf-8 -*-

#------------------------------------------------------
# versione Python 2



#RASPBERRY_AUDIO
#questa libreria contiene funzioni per la riproduzione di file audio su raspberry Pi

#------------------------------------------------------
import os


# gestire interfaccia audio di Raspberry: https://www.raspberrypi.org/documentation/usage/audio/README.mdaa
# utilizzo del modulo os: https://docs.python.org/2/library/os.html
def output_audio(messaggio):
    pid = os.forkpty()  # se non funziona usare pty.spawn()
    if (pid == 0):  # sono nel figlio
        {
            # SE DA QUALCHE PROBLEMA POTREBBE ESSERE PERCHE' NON HO FATTO FLUSH DEI PRECENTI INPUT (si risolve con la funzione os.fsync)
            os.exceclp("omxplayer", messaggio)  # eseguo il programma per la riproduzione dell'audio
        }