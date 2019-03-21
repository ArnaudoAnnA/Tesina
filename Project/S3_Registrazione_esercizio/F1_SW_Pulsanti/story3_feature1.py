
LETTERA_BOTTONE_SINISTRA = S
LETTERA_BOTTONE_CENTRALE = C
LETTERA_BOTTONE_DESTRA = D

TIMER_IN_IMPOSTAZIONE = 0
TIMER_IMPOSTATO_REGISTRAZIONE_ESERCIZIO = 1
TEMPO_FINITO = -1 


import time
import os #utilizzo del modulo os: https://docs.python.org/2/library/os.html
#in alternativa si può usare https://docs.python.org/2/library/pty.html#module-pty

print("  premi:\n   -C per tasto centrale\n  -S per tasto sinistra\n  -D per tasto destra\n")
lettera = input()	#https://www.geeksforgeeks.org/taking-input-from-console-in-python/
if(lettera == LETTERA_BOTTONE_SINISTRA)
	click_bottone_sinistra()
else if(lettera == LETTERA_BOTTONE_CENTRALE)
	click_bottone_centrale()
else if(lettera==LETTERA_BOTTONE_DESTRA)
	click_bottone_destra()


#la situazione inziale è "timer non impostato" e "esercizio non registrato"
statoTimer = TIMER_IN_IMPOSTAZIONE;
timer = 0
datasetEsercizio = [0]  #MOCK

#--------------------------------------------------------------------------------------------------------------------------------------------------	

def click_bottone_sinistra():
	if(statoTimer == TIMER_IN_IMPOSTAZIONE)
		if(timer!=0)
				timer= timer-1
				Timer_changed_listener.notify()				#funzione che si occuperà di dare in output tramite interfaccia audio il nuovo valore del timer

	else if(statoTimer == TIMER_IMPOSTATO_REGISTRAZIONE_ESERCIZIO)    #l'utente decide di scartare l'esercizio appena registrato
		output_audio(VALORE_SCARTATO)
		datasetEsercizio = [0] 
		timer = 0

#--------------------------------------------------------------------------------------------------------------------------------------------------		
		
def click_bottone_centrale():
	if(statoTimer == TIMER_IN_IMPOSTAZIONE and timer == 0)		#timer da impostare da capo (questo è il primo click sul tasto centrale)
		output_audio(SPIEGAZIONI_IMPOSTAZIONE_TIMER)
		
	else if(statoTimer == TIMER_IN_IMPOSTAZIONE and timer != 0) 	#l'utente ha terminato l'impostazione del timer
		statoTimer = TIMER_IMPOSTATO_REGISTRAZIONE_ESERCIZIO
		output_audio(CONFERMA_TIMER)
		registra_esercizio()

#--------------------------------------------------------------------------------------------------------------------------------------------------	
		
def click_bottone_destra():
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
