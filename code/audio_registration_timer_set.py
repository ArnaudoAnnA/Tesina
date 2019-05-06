# -*- coding: utf-8 -*-

#------------------------------------------------------
#Python 2

#IMPORTANT: needs the Rpy.GPIO module
#------------------------------------------------------

import audio_file_ita as audio
import RPi.GPIO as GPIO
import time
import audio_timer
import audio_raspberry as output_interface
import config

#constants
LEFT_BUTTON_PIN = config.LEFT_BUTTON_PIN
CENTRAL_BUTTON_PIN = config.CENTRAL_BUTTON_PIN
RIGHT_BUTTON_PIN = config.RIGHT_BUTTON_PIN

DIRECTORY_PATH = audio.DIRECTORY_PATH
NUMS = audio.NUMS
DISCARDED_VALUE = audio.DISCARDED_VALUE
TIMER_SETTINGS_GUIDE = audio.TIMER_SETTINGS_GUIDE
CONFIRM = audio.CONFIRM
SENDING_DATA = audio.SENDING_DATA
GO = audio.GO
REGISTRATION_ENDED = audio.REGISTRATION_ENDED
REGISTRATION_COMMENCES_IN_SECONDS = audio.REGISTRATION_COMMENCES_IN_SECONDS

ALL_OFF = 0
SETTING_TIMER = 1
TIMER_SET = 2

REGISTRATION_TIME_SPAN = 5


def left_button_click(channel):
    global timer_state
    if (timer_state == SETTING_TIMER):
        if (unset_timer.timer != 0):
            print(unset_timer.timer)
            unset_timer.increase_timer(-1)

    elif (timer_state == TIMER_SET):  # l'utente decide di scartare l'esercizio appena registrato
        output_interface.audio_output(DIRECTORY_PATH, DISCARDED_VALUE)
        exercise_dataset = [0]  #non è il caso di azzerare anche il timer perchè alla prossima pressione del tasto centrale verrà istanziato un nuovo oggetto timer
        timer_state = ALL_OFF

# --------------------------------------------------------------------------------------------------------------------------------------------------

def central_button_click(channel):
    global timer_state
    global unset_timer

    if ( timer_state == ALL_OFF):  # timer da impostare da capo (questo è il primo click sul tasto centrale)
        output_interface.output_audio(DISCARDED_VALUE, TIMER_SETTINGS_GUIDE)
        print("dovevo aver suonato")
        timer_state = SETTING_TIMER
        unset_timer = audio_timer.Timer(0)  #istazio un nuovo oggetto timer

    elif (timer_state == SETTING_TIMER and unset_timer.timer != 0):  # l'utente ha terminato l'impostazione del timer
        output_interface.output_audio(DIRECTORY_PATH, CONFIRM)
        timer_state = TIMER_SET


# --------------------------------------------------------------------------------------------------------------------------------------------------

def right_button_click(channel):
    global timer_state
    if (timer_state == SETTING_TIMER):
        print(unset_timer.timer)
        unset_timer.incrementaTimer(+1)

    elif (timer_state == TIMER_SET) : # l'utente decide di mantenere l'esercizio appena registrato
        output_interface.output_audio(DIRECTORY_PATH, SENDING_DATA)
        exercise_acquisition_audio()
        timer_state = ALL_OFF

# --------------------------------------------------------------------------------------------------------------------------------------------------
# thread che, contemporaneamente a quello che memorizza l'esercizio, scandisce il tempo

def exercise_acquisition_audio():

    output_interface.output_audio(DIRECTORY_PATH, REGISTRATION_COMMENCES_IN_SECONDS.format(REGISTRATION_TIME_SPAN))

    registration_countdown = audioTimer.Timer(DIRECTORY_PATH, REGISTRATION_TIME_SPAN)
    registration_countdown.audio_countdown(1)

    output_interface.audio_output(DIRECTORY_PATH, GO)
    time.sleep(1)

    unset_timer.audio_countdown(1)

    output_interface.audio_output(DIRECTORY_PATH, REGISTRATION_ENDED)


# ------- MAIN ----------------------------------------------------------------------------------------------------

GPIO.setmode(GPIO.BCM)                              #specifico quale configurazione di pin intendo usare
GPIO.setup(LEFT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #PUD_DOWN significa che, se non viene ricevuto nessun segnale da raspberry, l'input del pin è di default 0
                                                    #questa istruzione è importante per evitare errori dovuti a variazioni di tensione, che avvengono anche quando un pin non riceve voltaggio, per motivi fisici 
GPIO.setup(CENTRAL_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(RIGHT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#la situazione inziale è "timer non impostato" e "esercizio non registrato"
timer_state = ALL_OFF;
datasetEsercizio = [0]  #MOCK
unset_timer = audio_timer.Timer(0)

#aggiungo un event_detect ad ogni pin e associo la relativa funzione che gestirà l'evento click sul bottone
#ulteriori spiegazioni:  https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
#SINISTRA
GPIO.add_event_detect(LEFT_BUTTON_PIN, GPIO.FALLING)   #GPIO.FALLING significa che l'evento si scatena nel momento in cui il bottone viene premuto (non quando viene rilasciato)

GPIO.add_event_callback(LEFT_BUTTON_PIN, left_button_click)


#CENTRO
GPIO.add_event_detect(CENTRAL_BUTTON_PIN, GPIO.FALLING)
GPIO.add_event_callback(CENTRAL_BUTTON_PIN, central_button_click)

#DESTRA
GPIO.add_event_detect(RIGHT_BUTTON_PIN, GPIO.FALLING)
GPIO.add_event_callback(RIGHT_BUTTON_PIN, right_button_click)

while(True):
    pass
