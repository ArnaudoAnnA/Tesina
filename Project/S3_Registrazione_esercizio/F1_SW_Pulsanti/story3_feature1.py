
PIN_BOTTONE_SINISTRA = 3
PIN_BOTTONE_CENTRALE = 4
PIN_BOTTONE_DESTRA = 5

TIMER_IN_IMPOSTAZIONE = 0
TIMER_IMPOSTATO_REGISTRAZIONE_ESERCIZIO = 1
TEMPO_FINITO = -1 


import RPi.GPIO as GPIO 
import time
import os #utilizzo del modulo os: https://docs.python.org/2/library/os.html
#in alternativa si può usare https://docs.python.org/2/library/pty.html#module-pty

GPIO.setmode(GPIO.BCM) 								#specifico quale configurazione di pin intendo usare
GPIO.setup(PIN_BOTTONE_SINISTRA, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #PUD_DOWN significa che, se non viene ricevuto nessun segnale da raspberry, l'input del pin è di default 0
													#questa istruzione è importante per evitare errori dovuti a variazioni di tensione, che avvengono anche quando un pin non riceve voltaggio, per motivi fisici 
GPIO.setup(PIN_BOTTONE_CENTRALE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(PIN_BOTTONE_DESTRA, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#aggiungo un event_detect ad ogni pin e associo la relativa funzione che gestirà l'evento click sul bottone
#ulteriori spiegazioni:  https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
#SINISTRA
GPIO.add_event_detect(PIN_BOTTONE_SINISTRA, GPIO.FALLING) 	#GPIO.FALLING significa che l'evento si scatena nel momento in cui il bottone viene premuto (non quando viene rilasciato)

GPIO.add_event_callback(PIN_BOTTONE_SINISTRA, click_bottone_sinistra)


#CENTRO
GPIO.add_event_detect(PIN_BOTTONE_CENTRALE, GPIO.FALLING)
GPIO.add_event_callback(PIN_BOTTONE_CENTRALE, click_bottone_centrale)

#DESTRA
GPIO.add_event_detect(PIN_BOTTONE_DESTRA, GPIO.FALLING)
GPIO.add_event_callback(PIN_BOTTONE_DESTRA, click_bottone_destra)


#la situazione inziale è "timer non impostato" e "esercizio non registrato"
statoTimer = TIMER_IN_IMPOSTAZIONE;
timer = 0
datasetEsercizio = [0]  #MOK

#--------------------------------------------------------------------------------------------------------------------------------------------------	

def click_bottone_sinistra(channel):
	if(statoTimer == TIMER_IN_IMPOSTAZIONE)
		if(timer!=0)
				timer= timer-1
				Timer_changed_listener.notify()				#funzione che si occuperà di dare in output tramite interfaccia audio il nuovo valore del timer

	else if(statoTimer == TIMER_IMPOSTATO_REGISTRAZIONE_ESERCIZIO)    #l'utente decide di scartare l'esercizio appena registrato
		output_audio(VALORE_SCARTATO)
		datasetEsercizio = [0] 
		timer = 0

#--------------------------------------------------------------------------------------------------------------------------------------------------		
		
def click_bottone_centrale(channel):
	if(statoTimer == TIMER_IN_IMPOSTAZIONE and timer == 0)		#timer da impostare da capo (questo è il primo click sul tasto centrale)
		output_audio(SPIEGAZIONI_IMPOSTAZIONE_TIMER)
		
	else if(statoTimer == TIMER_IN_IMPOSTAZIONE and timer != 0) 	#l'utente ha terminato l'impostazione del timer
		statoTimer = TIMER_IMPOSTATO_REGISTRAZIONE_ESERCIZIO
		output_audio(CONFERMA_TIMER)
		registra_esercizio()

#--------------------------------------------------------------------------------------------------------------------------------------------------	
		
def click_bottone_destra(channel):
	if(statoTimer == TIMER_IN_IMPOSTAZIONE)
		timer = timer +1
		Timer_changed_listener.notify()	
		
	else if(statoTimer == TIMER_IMPOSTATO_REGISTRAZIONE_ESERCIZIO)    #l'utente decide di mantenere l'esercizio appena registrato	
		output_audio(INVIO_DATI_IN_CORSO)
		invia_al_server(datasetEsercizio)	# MOK STORY6


#--------------------------------------------------------------------------------------------------------------------------------------------------	

class Timer_changed_listener:
	
	def notify()	#metodo statico. 
					#viene evocato ogni volta che il numero del timer cambia
					#da in output il nuovo valore del timer.
					#se il nuovo valore è 0, restituisce TEMPO_FINITO, che può essere ignorato o meno a seconda di dove viene richiamato il metodo
		output_audio(timer)	
		if(timer == 0)
			return TEMPO_FINITO

#--------------------------------------------------------------------------------------------------------------------------------------------------	
#thread che, contemporaneamente a quello che memorizza l'esercizio, scandisce il tempo

def registra_esercizio():
	while Timer_changed_listener.notify() != TEMPO_FINITO:
		timer = timer -1
		time.sleep(1)	#aspetto un secondo			

		
#--------------------------------------------------------------------------------------------------------------------------------------------------	
#gestire interfaccia audio di Raspberry: https://www.raspberrypi.org/documentation/usage/audio/README.mdaa
#utilizzo del modulo os: https://docs.python.org/2/library/os.html
def output_audio(messaggio):
	pid = os.forkpty() 	#se non funziona usare pty.spawn()
	if(pid==0) 		#sono nel figlio
	{
		#SE DA QUALCHE PROBLEMA POTREBBE ESSERE PERCHE' NON HO FATTO FLUSH DEI PRECENTI INPUT (si risolve con la funzione os.fsync)
		os.exceclp("omxplayer", messaggio)	#eseguo il programma per la riproduzione dell'audio	
	}	
