# -*- coding : utf-8 -*-

import time
import db_functions
import audio_raspberry as output_interface
import audio_file_ita as audio
import table_exercises
import audio_feedback_exercise



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
	global state
	global id_current_exercise
	
	if(state == SELECTING):
		if(id_current_exercise == 0):
                	id_current_exercise = n_exercises - 1
                else:
                	id_current_exercise = id_current_exercise - 1
			
		current_exercise = exercises[id_current_exercise]
		
		#do in output la descrizione dell'exercise corrente
		output_interface.audio_output([EXERCISE + NUMBERS[id_current_exercise]])
		time.sleep(0.5)
		audio_index = db_functions.table_exercises.COLUMNS.index(db_functions.table_exercises.COLUMN_AUDIO)
		output_interface.audio_output([current_exercise[audio_index]])
		
	elif(state == CONFIRM_REQUEST):
		#ritorno in modalità SELECTING 
		state = SELECTING


		
def central_button_click(channel):
	global state
	global exercises
	global n_exercises
	
	if(state == EXERCISE_NOT_SELECTED): 	#primo click sul bottone centrale 
		#scarico le descrizioni di tutti gli exercises e li metto a disposizione dell'utente per la selezione
		#mi connetto al DB
		dbConn = db_functions.Database.db_connect()
		exercises = db_functions.table_exercises.get_all_exercises(dbConn)

		if(exercises == None):
			output_interface.audio_output([NO_AVAIABLE_EXERCISE])
		
		else:
			n_exercises = len(exercises)
			output_interface.audio_output([USE_THE_ARROWS_TO_SELECT_THE_EXERCISE])
			state = SELECTING
	
	elif(state == SELECTING):
		output_interface.audio_output(CONFIRM)
		state = CONFIRM_REQUEST

		
def click_bottone_destra(channel):
	global state
	global exercises
	global n_exercises
	global state
	global id_current_exercise
	
	if(state == SELECTING):
		id_current_exercise = id_current_exercise + 1 % n_exercises
		current_exercise = exercises[id_current_exercise]
		
		#do in output la descrizione dell'exerciseso corrente
		output_interface.audio_output([EXERCISE, NUMBERS[id_current_exercise]])
		time.sleep(0.5)
		audio_index = db_functions.table_exercises.COLUMNS.index(table_exercises.COLUMN_AUDIO)
		output_interface.audio_output([current_exercise[audio_index]])		
	elif(state == CONFIRM_REQUEST):
		#l'utente ha selezionato l'exerciseso: richiamo le funzioni che gestiscono l'esecuzione dell'exerciseso
			#per prima cosa recupero tutti i dati relativi all'exerciseso selezionato
			sensors = table_sensors.get_sensors()
			
			index_duration_seconds = db_functions.table_exercises.COLUMNS.index(db_functions.table_exercises.COLUMN_TIME_SECONDS)
			exerciseso = exercises[id_current_exercise]
			duration_seconds = exerciseso[index_duration_seconds]

			#faccio partire il timer che scandisce il tempo dell'exerciseso
			AudioFeedbackExercise.outputTimer(duration_seconds)

			# avvio i thread che leggono dai sensors e eseguono l'algoritmo di intelligenza artificiale
	
	
	
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
exercises = None
n_exercises = None
id_current_exercise = 0

while(True):
    pass	
