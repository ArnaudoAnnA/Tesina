# -*- coding: utf-8 -*-

#------------------------------------------------------
#Python 2

#IMPORTANT: needs the Rpy.GPIO module
#------------------------------------------------------

import audio_file_ita as file_audio
import RPi.GPIO as GPIO
import time
import audio_timer
import audio_raspberry as output_interface
import config

#constants
LEFT_BUTTON_PIN = config.LEFT_BUTTON_PIN
CENTRAL_BUTTON_PIN = config.CENTRAL_BUTTON_PIN
RIGHT_BUTTON_PIN = config.RIGHT_BUTTON_PIN

ALL_OFF = 0
SETTING_TIMER = 1
TIMER_SET = 2

TIME_BEFORE_START = 5


def left_button_click(channel):
    global timer_state
    global unset_timer
    
    if (timer_state == SETTING_TIMER):
        if (unset_timer.timer != 0):
            print(unset_timer.timer)
            unset_timer.increase_timer(-1)

    elif (timer_state == TIMER_SET):  # l'utente decide di scartare l'esercizio appena registrato
        output_interface.audio_output(file_audio.DIRECTORY_PATH, file_audio.VALORE_SCARTATO)
        exercise_dataset = [0]  #non è il caso di azzerare anche il timer perchè alla prossima pressione del tasto centrale verrà istanziato un nuovo oggetto timer
        timer_state = ALL_OFF

# --------------------------------------------------------------------------------------------------------------------------------------------------

def central_button_click(channel):
    global timer_state
    global unset_timer

    if ( timer_state == ALL_OFF):  # timer da impostare da capo (questo è il primo click sul tasto centrale)
        output_interface.output_audio(file_audio.DISCARDED_VALUE, file_audio.ISTRUZIONI_IMPOSTAZIONE_TIMER)
        timer_state = SETTING_TIMER
        unset_timer = audio_timer.Timer(0)  #istazio un nuovo oggetto timer

    elif (timer_state == SETTING_TIMER and unset_timer.timer != 0):  # l'utente ha terminato l'impostazione del timer
        output_interface.output_audio(file_audio.DIRECTORY_PATH, file_audio.CONFERMARE_NUMERO)
        timer_state = TIMER_SET


# --------------------------------------------------------------------------------------------------------------------------------------------------

def right_button_click(channel):
    global timer_state
    global unset_timer
    
    if (timer_state == SETTING_TIMER):
        print(unset_timer.timer)
        unset_timer.increase_timer(+1)

    elif (timer_state == TIMER_SET) : # l'utente conferma il tempo impostato e procede con la registrazione dell'esercizio
        exercise_acquisition_audio()
        #volendo qui si può aggiungere una richiesta al'utente se intende salvare l'esercizio appena registrato
        timer_state = ALL_OFF

# --------------------------------------------------------------------------------------------------------------------------------------------------
# thread che, contemporaneamente a quello che memorizza l'esercizio, scandisce il tempo

def exercise_acquisition_audio():

    output_interface.output_audio(file_audio.DIRECTORY_PATH, file_audio.REGISTRAZIONE_AVVIATA_TRA.format(REGISTRATION_TIME_SPAN))

    registration_countdown = audioTimer.Timer(TIME_BEFORE_START)
    registration_countdown.audio_countdown(1)

    output_interface.audio_output(file_audio.DIRECTORY_PATH, file_audio.VIA)
    time.sleep(1)

    unset_timer.audio_countdown(1)

    output_interface.audio_output(file_audio.DIRECTORY_PATH, file_audio.REGISTRAZIONE_TERMINATA)


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
