# -*- coding: utf-8 -*-

#------------------------------------------------------
# versione Python 2

#RASPBERRY_AUDIO
#function for playing audio on raspberry 
#given the absolute path of the file.

#------------------------------------------------------
import pygame

# gestire interfaccia audio di Raspberry: https://www.raspberrypi.org/documentation/usage/audio/README.mdaa

def output_audio(path, file_audio):
    pygame.init()
    audio = pygame.mixer.Sound(file_audio)
    audio.play()
