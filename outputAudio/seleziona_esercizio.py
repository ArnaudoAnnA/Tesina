# -*- coding : utf-8 -*-

import time
import funzioniDB
import raspberry_audio as output_interface
import FILE_AUDIO 
import Table_Exercises
import audio_feedback_esercizio 

#COSTANTI
ESERCIZIO_NON_SELEZIONATO = 0
IN_SELEZIONE = 1
RICHIESTA_CONFERMA = 2



def click_bottone_sinistra(channel):
	global situazione
	global idEsercizioCorrente
	
	if(situazione == IN_SELEZIONE):
		idEsercizioCorrente = idEsercizioCorrente + 1 % nEsercizi
		esercizioCorrente = esercizi[idEsercizioCorrente]
		
		#do in output la descrizione dell'esercizio corrente
		output_interface.output_audio(FILE_AUDIO.ESERCIZIO + FILE_AUDIO.numeri[idEsercizioCorrente])
		time.sleep(0.5)
		indiceAudio = Table_Exercises.COLUMNS.index(Table_Exercises.COLUMN_AUDIO)
		output_interface.output_audio(esercizioCorrente[indiceAudio])
		
	elif(situazione == RICHIESTA_CONFERMA):
		#ritorno in modalità IN_SELEZIONE 
		situazione = IN_SELEZIONE


		
def click_bottone_centrale(channel):
	global situazione
	global esercizi
	global nEsercizi
	
	if(situazione == ESERCIZIO_NON_SELEZIONATO): 	#primo click sul bottone centrale 
		#scarico le descrizioni di tutti gli esercizi e li metto a disposizione dell'utente per la selezione
		#mi connetto al DB
		dbConn = funzioniDB.Database.db_connect()
		esercizi = funzioniDB.Table_Exercises.getAllExcercises()

		if(esercizi == NULL):
			output_interface.output_audio(FILE_AUDIO.NESSUN_ESERCIZIO_DISPONIBILE)
		
		else:
			nEsercizi = len(esercizi)
			output_interface.output_audio(FILE_AUDIO.USARE_FRECCIE_PER_SELEZIONARE_ESERCIZIO)
			situazione = IN_IMPOSTAZIONE
	
	elif(situazione == IN_IMPOSTAZIONE):
		output_interface.output_audio(FILE_AUDIO.CONFERMA)
		situazione = RICHIESTA_CONFERMA

		
def click_bottone_destra(channel):
	global situazione
	global esercizio
	
	global situazione
	global idEsercizioCorrente
	
	if(situazione == IN_SELEZIONE and idEsercizioCorrente > 0):
		idEsercizioCorrente = idEsercizioCorrente - 1
		esercizioCorrente = esercizi[idEsercizioCorrente]
		
		#do in output la descrizione dell'esercizio corrente
		output_interface.output_audio(FILE_AUDIO.ESERCIZIO + FILE_AUDIO.numeri[idEsercizioCorrente])
		time.sleep(0.5)
		indiceAudio = Table_Exercises.COLUMNS.index(Table_Exercises.COLUMN_AUDIO)
		output_interface.output_audio(esercizioCorrente[indiceAudio])
		
	elif(situazione == RICHIESTA_CONFERMA):
		#l'utente ha selezionato l'esercizio: richiamo le funzioni che gestiscono l'esecuzione dell'esercizio
			#per prima cosa recupero tutti i dati relativi all'esercizio selezionato
			sensori = Table_sensors.get_sensors()
			indiceDurataSecondi = Table_Exercises.COLUMNS.index(Table_Exercises.COLUMN_DURATA_SECONDI)
			durataSecondi = esercizio[indiceDurataSecondi]

			#faccio partire il timer che scandisce il tempo dell'esercizio
			audio_feedback_esercizio.outputTimer(durataSecondi)

			# avvio i thread che leggono dai sensori e eseguono l'algoritmo di intelligenza artificiale
	
	
	
#---------------------------------------------------------------------------------------
#MAIN
	
#SETUP DEI BOTTONI
	
GPIO.setmode(GPIO.BCM)                              #specifico quale configurazione di pin intendo usare
GPIO.setup(config.PIN_BOTTONE_SINISTRA, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #PUD_DOWN significa che, se non viene ricevuto nessun segnale da raspberry, l'input del pin è di default 0
                                                    #questa istruzione è importante per evitare errori dovuti a variazioni di tensione, che avvengono anche quando un pin non riceve voltaggio, per motivi fisici 
GPIO.setup(config.PIN_BOTTONE_CENTRALE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(config.PIN_BOTTONE_DESTRA, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#aggiungo un event_detect ad ogni pin e associo la relativa funzione che gestirà l'evento click sul bottone
#ulteriori spiegazioni:  https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
#SINISTRA
GPIO.add_event_detect(config.PIN_BOTTONE_SINISTRA, GPIO.FALLING)   #GPIO.FALLING significa che l'evento si scatena nel momento in cui il bottone viene premuto (non quando viene rilasciato)
GPIO.add_event_callback(config.PIN_BOTTONE_SINISTRA, click_bottone_sinistra)

#CENTRO
GPIO.add_event_detect(config.PIN_BOTTONE_CENTRALE, GPIO.FALLING)
GPIO.add_event_callback(config.PIN_BOTTONE_CENTRALE, click_bottone_centrale)

#DESTRA
GPIO.add_event_detect(config.PIN_BOTTONE_DESTRA, GPIO.FALLING)
GPIO.add_event_callback(config.PIN_BOTTONE_DESTRA, click_bottone_destra)


#situazione iniziale: ESERCIZIO NON SELEZIONATO
situazione = ESERCIZIO_NON_SELEZIONATO
esercizi = None
nEsercizi = None
idEsercizioCorrente = -1

while(True):
    pass	
