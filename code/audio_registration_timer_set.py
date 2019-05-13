# -*- coding: utf-8 -*-

#------------------------------------------------------
#Python 2

#IMPORTANT: needs the Rpy.GPIO module
#------------------------------------------------------

import audio_file_ita as audio_files
import RPi.GPIO as GPIO
import threading
import audio_timer
import audio_raspberry as output_interface
import config

#constants
LEFT_BUTTON_PIN 	= config.LEFT_BUTTON_PIN
CENTRAL_BUTTON_PIN 	= config.CENTRAL_BUTTON_PIN
RIGHT_BUTTON_PIN 	= config.RIGHT_BUTTON_PIN

ALL_OFF 			= 0
SETTING_NUMBER			= 1
WAITING_CONFIRM			= 2

class Get_number_from_user:
""" class that uses an timer object (improprially) to allow user to select a number using buttons"""	

	state 	= ALL_OFF
	timer_object 	= audio_timer.Timer(0)
	confirm 	= False
	
	def __init__(self):
		
		state = ALL_OFF
		timer_object = audio_timer.Timer(0)
		confirm = False
		
		GPIO.setmode(GPIO.BCM)                              #specifico quale configurazione di pin intendo usare
	    	GPIO.setup(LEFT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #PUD_DOWN significa che, se non viene ricevuto nessun segnale da raspberry, l'input del pin è di default 0
	                                                        #questa istruzione è importante per evitare errori dovuti a variazioni di tensione, che avvengono anche quando un pin non riceve voltaggio, per motivi fisici 
	   	GPIO.setup(CENTRAL_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	    	GPIO.setup(RIGHT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

	#------------------------------------------------------------------------------------------------------------------------------------	

	def left_button_click(self, channel):
	"""left button means:
		-user want to decrease the number
		-user wants to discard current number
	 	it depens from "state" variable """
  
	    if (self.state == SETTING_NUMBER):
	        if (self.timer_object.timer != 0):
	            print(self.timer_object.timer)
	            self.timer_object.increase_timer(-1)

	    elif (self.state == WAITING_CONFIRM):  # l'utente decide di scartare l'esercizio appena registrato
	        output_interface.audio_output(audio_files.DIRECTORY_PATH, [audio_files.DISCARDED_VALUE])
	        exercise_dataset = [0]  #non è il caso di azzerare anche il timer perchè alla prossima pressione del tasto centrale verrà istanziato un nuovo oggetto timer
	        self.state = ALL_OFF

	# --------------------------------------------------------------------------------------------------------------------------------------------------

	def central_button_click(self, channel):
	""" central button means:
		-user want to start setting the number -> I give him the instructions
		-user has selected a number and want to confirm it
		it depends from the value of the "state" variable """

	    if ( self.state == ALL_OFF):  # timer da impostare da capo (questo è il primo click sul tasto centrale)
	        output_interface.output_audio(audio_files.DISCARDED_VALUE, [audio_files.WAITING_CONFIRMTINGS_GUIDE])
	        self.state = SETTING_NUMBER
	        self.timer_object = audio_timer.Timer(0)  #istazio un nuovo oggetto timer

	    elif (self.state == SETTING_NUMBER and self.timer_object.timer != 0):  # l'utente ha terminato l'impostazione del timer
	        output_interface.output_audio(audio_files.DIRECTORY_PATH, [audio_files.CONFIRM])
	        self.state = WAITING_CONFIRM


	# --------------------------------------------------------------------------------------------------------------------------------------------------

	def right_button_click(self, channel):
	""" right button means:
		-user want to increase the number
		-user confirmed the selected number
		it depends from the value of the "state" variable """	
	    
	    if (self.state == SETTING_NUMBER):
	        print(self.timer_object.timer)
	        self.timer_object.increase_timer(+1)

	    elif (self.state == WAITING_CONFIRM) : # l'utente conferma il tempo impostato e procede con la registrazione dell'esercizio
	        self.confirm = 1
	        self.state = ALL_OFF

	# --------------------------------------------------------------------------------------------------------------------------------------------------
	def get_number():
	""" returns the value of the timer more easly"""
		return self.timer_object.timer

	# ------- MAIN ---------------------------------------------------------------------------------------------------

	def set_pins_and_start(self):
	"""this is the main function because add an event listener (i.e. a functions described below) 
		on each button. Then that functions loops until a number is selected and confirmed by the user.
		NOTE: each event listener function is executed by a thread"""
	
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

	    while(self.confirm==0):
	        pass
	
#----THREAD VERSION------------------------------------------------------------------------------------	
class Thread_get_number(Get_number_from_user, threading.Thread):
"""class that makes the method "set_pins_and_start" executed in a new thread"""	

	def __init__(self):
		threading.Thread.__init__(self)
		Get_number_from_user.__init__(self)
		
	def run(self)
		set_pins_and_start()
		#thread exits when this function returns
