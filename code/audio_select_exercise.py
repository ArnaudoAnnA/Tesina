# -*- coding : utf-8 -*-

import time
import db_functions
import audio_raspberry as output_interface
import audio_file_ita as audio
import table_exercises
import audio_feedback_exercise
import audio_registration_timer_set


#constants
LEFT_BUTTON_PIN = config.LEFT_BUTTON_PIN
CENTRAL_BUTTON_PIN = config.CENTRAL_BUTTON_PIN
RIGHT_BUTTON_PIN = config.RIGHT_BUTTON_PIN

DIRECTORY_PATH = audio.DIRECTORY_PATH
NUMS = audio.NUMS
CONFIRM = audio.CONFIRM
GO = audio.GO
NO_AVAIABLE_EXERCISE = audio.NO_AVAIABLE_EXERCISE
USE_THE_ARROWS_TO_SELECT_THE_EXERCISE = audio.USE_THE_ARROWS_TO_SELECT_THE_EXERCISE

AudioFeedbackExercise = audio_feedback_exercise.AudioFeedbackExercise

EXERCISE_NOT_SELECTED = 0
SELECTING = 1
CONFIRM_REQUEST = 2



def left_button_click(channel):
	global audio_index
	global id_exercise_index
	
	global state
	global array_exercises
	global array_exercises_iterator
	
	
	if(state == SELECTING):
		if(id_current_exercise == 0):
                	array_exercises_iterator = array_exercises.length -1
                else:
                	array_exercises_iterator -=1
			
		#I get the current exercise from the array	
		current_exercise = exercises[array_exercises_iterator]
		id_current_exercise = current_exercise[id_exercise_index]
		
		#do in output la descrizione dell'exercise corrente
		output_interface.audio_output([EXERCISE, NUMBERS[id_current_exercise]])
		time.sleep(0.5)
		output_interface.audio_output([current_exercise[audio_index]])
		
	elif(state == CONFIRM_REQUEST):
		#ritorno in modalità SELECTING 
		state = SELECTING


		
def central_button_click(channel):
	global state
	global array_exercises
	
	global audio_index
	global id_exercise_index
	
	if(state == EXERCISE_NOT_SELECTED): 	#primo click sul bottone centrale 
		#scarico le descrizioni di tutti gli exercises e li metto a disposizione dell'utente per la selezione
		#mi connetto al DB
		db = db_functions.Database()
		#all data of the exercise is saved in an array format, so I have to know what correspond to each index
		audio_index = db.table_exercises.get_column_index(db.table_exercises.COLUMN_AUDIO)
		id_exercise_index = db.table_exercises.get_column_index(db.table_exercises.COLUMN_ID_EXERCISE)
		
		array_exercises = db.table_exercises.get_all_exercises()

		if(exercises == None):
			output_interface.audio_output([NO_AVAIABLE_EXERCISE])
		
		else:
			state = SELECTING
			output_interface.audio_output([USE_THE_ARROWS_TO_SELECT_THE_EXERCISE])
			
	
	elif(state == SELECTING):
		state = CONFIRM_REQUEST
		output_interface.audio_output(CONFIRM)

		
def click_bottone_destra(channel):
	global audio_index
	global id_exercise_index
	
	global state
	
	global array_exercises
	global array_exercises_iterator
	
	if(state == SELECTING):
		array_exercises_iterator = array_exercises_iterator + 1 % array_exercises.length
		
		#I get the current exercise form the array
		current_exercise = array_exercises[array_exercises_iterator]
		id_current_exercise = current_exercise[id_exercise_index]
		
		#do in output la descrizione dell'exerciseso corrente
		output_interface.audio_output([EXERCISE, NUMBERS[id_current_exercise]])
		time.sleep(0.5)
		output_interface.audio_output([current_exercise[audio_index]])	
		
	elif(state == CONFIRM_REQUEST):
		#l'utente ha selezionato l'exerciseso: richiamo le funzioni che gestiscono l'esecuzione dell'exerciseso
		#per prima cosa recupero tutti i dati relativi all'esercizio selezionato
		exercise = array_exercises[array_exercises_iterator]

		#Asking to the user how long he want to do the exercise
		audio_registration_timer_set.set_timer(audio_feedback_exercise.AudioFeedBackExercise.outputTimer)
		
		#when the user set the duration of the esecution, an audio timer start the cuntdown while one thread 
		#for each sensor recognises the exercise

	
	
#---------------------------------------------------------------------------------------
#MAIN
	
#SETUP DEI BOTTONI
	
GPIO.setmode(GPIO.BCM)                              #specifico quale configurazione di pin intendo usare
GPIO.setup(LEFT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #PUD_DOWN significa che, se non viene ricevuto nessun segnale da raspberry, l'input del pin è di default 0
                                                    #questa istruzione è importante per evitare errori dovuti a variazioni di tensione, che avvengono anche quando un pin non riceve voltaggio, per motivi fisici 
GPIO.setup(CENTRAL_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(RIGHT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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


#state iniziale: ESERCIZIO NON SELEZIONATO
state = EXERCISE_NOT_SELECTED
array_exercises = None
array_exercises_iterator = 0
audio_index = None
id_exercise_index = None


while(True):
    pass	
