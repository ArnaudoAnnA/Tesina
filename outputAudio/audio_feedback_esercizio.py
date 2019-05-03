
# -*- coding: utf-8 -*-

import time
import audio_timer
import raspberry_audio as outputInterface
import FILE_AUDIO

TEMPO_PRE_INIZIO_CORREZIONE = 5
MINIMO_PERCENTUALE_CORRETTEZZA = 65

class AudioFeedBackEsercizio:
  
  sommaCorrettezza = 0
  n_feedBack = 0

  #funzione che si occupa del timer durante la fase di correzione esercizio
  @staticmethod
  def outputTimer(tempo):
    AudioFeedBackEsercizio.correttezzaMedia = 0
    AudioFeedBackEsercizio.n_feedback = 0
    timer = audio_timer.Timer(tempo)

    #conto alla rovescia prima dell'inizio 
    timer_pre = audio_timer.Timer(TEMPO_PRE_INIZIO_CORREZIONE)
    outputInterface.output_audio(FILE_AUDIO.INIZIO_REGISTRAZIONE_TRA_QUALCHE_SECONDO.format(TEMPO_PRE_INIZIO_REGISTRAZIONE))
    timer_pre.audio_conto_alla_rovescia(1)

    #inizio della fase di acquisizione e correzione
    outputInterface.output_audio(FILE_AUDIO.VIA)                                                        #"via"
    time.sleep(1)
    timer.audio_conto_alla_rovescia(1)  
    
    #alla fine, do in output il resoconto dell'esecuzione dell'esercizio
    correttezzaMedia = AudioFeedBackEsercizio.correttezzaMedia / AudioFeedBackEsercizio.n_feedBack  #VOLENDO SI PUO' DARE IN OUTPUT LA CORRETTEZZA MEDIA PER SENSORE
    outputInterface.outputAudio(FILE_AUDIO.RESOCONTO_ESERCIZIO.format(correttezzaMedia))


  #funzione richiamata dai thread ogni volta che l'algoritmo di intelligenza artificiale riconosce un movimento
  @staticmethod
  def feedback_movimento_notify(sensore, percentualeCorrettezza):

    if(percentualeCorrettezza < MINIMO_PERCENTUALE_CORRETTEZZA):
      outputInterface.output_audio(FILE_AUDIO.FEEDBACK_ERRORE.format(sensore))
  
    #salvo i dati per il resoconto
    AudioFeedBackEsercizio.sommaCorrettezza += percentualeCorrettezza
    AudioFeedBackEsercizio.n_feedBack += 1
