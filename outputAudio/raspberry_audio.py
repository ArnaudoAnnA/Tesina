
# -*- coding: utf-8 -*-

#------------------------------------------------------
# versione Python 2



#RASPBERRY_AUDIO
#questo modulo contiene funzioni per la riproduzione di file audio su raspberry Pi

#------------------------------------------------------
import os

# gestire interfaccia audio di Raspberry: https://www.raspberrypi.org/documentation/usage/audio/README.mdaa
# utilizzo del modulo os: https://docs.python.org/2/library/os.html
# utilizzo del modulo subprocess : https://docs.python.org/2/library/subprocess.html
def output_audio(messaggio):
   cmd = "omxplayer "+messaggio
   os.system(cmd)
