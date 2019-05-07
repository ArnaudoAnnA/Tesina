# -*- coding: utf-8 -*-

#------------------------------------------------------
# versione Python 2

#RASPBERRY_AUDIO
#function for playing audio on raspberry 
#given the absolute path of the file.

#------------------------------------------------------
import pygame

# gestire interfaccia audio di Raspberry: https://www.raspberrypi.org/documentation/usage/audio/README.mdaa

def output_audio(path, files_audio):
    pygame.init()
    
    for file in files_audio:
        audio = pygame.mixer.Sound(file)
        audio.play()
        
        while(pygame.mixer.get_buisy()):    #I wait for the end of the audio reproduction
            pass
