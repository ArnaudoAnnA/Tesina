# -*- coding: utf-8 -*-

#------------------------------------------------------
#Python 2

#IMPORTANT: needs the Rpy.GPIO module
#------------------------------------------------------

import audio_file_ita as audio_files
import RPi.GPIO as GPIO
import time
import audio_timer
import audio_raspberry as output_interface
import config

#constants
LEFT_BUTTON_PIN 	= config.LEFT_BUTTON_PIN
CENTRAL_BUTTON_PIN 	= config.CENTRAL_BUTTON_PIN
RIGHT_BUTTON_PIN 	= config.RIGHT_BUTTON_PIN

ALL_OFF 			= config.REGISTRATION_ALL_OFF
SETTING_TIMER		= config.REGISTRATION_SETTING_TIMER
TIMER_SET			= config.REGISTRATION_TIMER_SET

TIME_BEFORE_START 	= config.REGISTRATION_TIME_BEFORE_START

class SetNumber:

	timer_state 	= 0
	timer_object 	= None
	confirm 		= 0

	def left_button_click(self, channel):
  
	    if (self.timer_state == SETTING_TIMER):
	        if (self.timer_object.timer != 0):
	            print(self.timer_object.timer)
	            self.timer_object.increase_timer(-1)

	    elif (self.timer_state == TIMER_SET):  # l'utente decide di scartare l'esercizio appena registrato
	        output_interface.audio_output(audio_files.DIRECTORY_PATH, [audio_files.DISCARDED_VALUE])
	        exercise_dataset = [0]  #non è il caso di azzerare anche il timer perchè alla prossima pressione del tasto centrale verrà istanziato un nuovo oggetto timer
	        self.timer_state = ALL_OFF

	# --------------------------------------------------------------------------------------------------------------------------------------------------

	def central_button_click(self, channel):

	    if ( self.timer_state == ALL_OFF):  # timer da impostare da capo (questo è il primo click sul tasto centrale)
	        output_interface.output_audio(audio_files.DISCARDED_VALUE, [audio_files.TIMER_SETTINGS_GUIDE])
	        self.timer_state = SETTING_TIMER
	        self.timer_object = audio_timer.Timer(0)  #istazio un nuovo oggetto timer

	    elif (self.timer_state == SETTING_TIMER and self.timer_object.timer != 0):  # l'utente ha terminato l'impostazione del timer
	        output_interface.output_audio(audio_files.DIRECTORY_PATH, [audio_files.CONFIRM])
	        self.timer_state = TIMER_SET


	# --------------------------------------------------------------------------------------------------------------------------------------------------

	def right_button_click(self, channel):
	    
	    if (self.timer_state == SETTING_TIMER):
	        print(self.timer_object.timer)
	        self.timer_object.increase_timer(+1)

	    elif (self.timer_state == TIMER_SET) : # l'utente conferma il tempo impostato e procede con la registrazione dell'esercizio
	        self.confirm = 1
	        self.timer_state = ALL_OFF

	# --------------------------------------------------------------------------------------------------------------------------------------------------
	# returns the value of the timer
	def get_number():
		return self.timer_object.timer

	# ------- MAIN ---------------------------------------------------------------------------------------------------
	#globals
	self.timer_state = ALL_OFF
	self.timer_object = audio_timer.Timer(0)
	callback = None

	#NOTE: when the timer is setted, a callback function is called
	def set_timer(self, callback_when_timer_setted):
	    GPIO.setmode(GPIO.BCM)                              #specifico quale configurazione di pin intendo usare
	    GPIO.setup(LEFT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #PUD_DOWN significa che, se non viene ricevuto nessun segnale da raspberry, l'input del pin è di default 0
	                                                        #questa istruzione è importante per evitare errori dovuti a variazioni di tensione, che avvengono anche quando un pin non riceve voltaggio, per motivi fisici 
	    GPIO.setup(CENTRAL_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	    GPIO.setup(RIGHT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

	    #la situazione inziale è "timer non impostato" e "esercizio non registrato"
	    self.timer_state = ALL_OFF;
	    self.timer_object = audio_timer.Timer(0)
	    callback = callback_when_timer_setted

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
