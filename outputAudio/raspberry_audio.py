
# -*- coding: utf-8 -*-

#------------------------------------------------------
# versione Python 2



#RASPBERRY_AUDIO
#questa libreria contiene funzioni per la riproduzione di file audio su raspberry Pi

#------------------------------------------------------
import soundplayer

ID_AUDIOOUTPUT_DEVICE = 1


# gestire interfaccia audio di Raspberry: https://www.raspberrypi.org/documentation/usage/audio/README.mdaa
# utilizzo del modulo os: https://docs.python.org/2/library/os.html
# utilizzo del modulo subprocess : https://docs.python.org/2/library/subprocess.html
def output_audio(messaggio):
   p = soundplayer.SoundPlayer(messaggio, ID_AUDIOOUTPUT_DEVICE)
   p.play()
