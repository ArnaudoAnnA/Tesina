# -*- coding: utf-8 -*-

#------------------------------------------------------
# versione Python 2



#AUDIO_TIMER
#questa libreria implementa un timer audio. Il timer è audio nel senso che ogni volta che cambia il suo valore,
#il nuovo valore viene dato in output tramite l'interfaccia audio

#------------------------------------------------------

#costanti
TEMPO_FINITO = -1

import time
import FILE_AUDIO
import raspberry_audio as audioInterface


class Timer:
    timer = 0

    def __init__(self, valoreIniziale):
        self.timer = valoreIniziale


    def impostaTimer(self, nuovo):
        self.timer = nuovo
        return Timer_changed_listener.notify(self.timer)

    # --------------------------------------------------------------------------------------------------------------------------------------
    def incrementaTimer(self, incremento):
		self.timer = self.timer + incremento
		return Timer_changed_listener.notify(self.timer)
    #------------------------------------------------------------------------------------------------------------------------------------
    def audio_conto_alla_rovescia(self, intervalloOgniQuantoNotificare):
        while self.incrementaTimer(-intervalloOgniQuantoNotificare) != TEMPO_FINITO:
            time.sleep(intervalloOgniQuantoNotificare)  # aspetto 

    # --------------------------------------------------------------------------------------------------------------------------------------------------




# --------------------------------------------------------------------------------------------------------------------------------------------------

class Timer_changed_listener:

    @staticmethod
    def notify(timer):  # metodo statico.
        # viene evocato ogni volta che il numero del timer cambia
        # da in output il nuovo valore del timer.
        # se il nuovo valore è 0, restituisce TEMPO_FINITO, che può essere ignorato o meno a seconda di dove viene richiamato il metodo
        audioInterface.output_audio(FILE_AUDIO.PATH_CARTELLA + FILE_AUDIO.numeri[timer])
        if (timer == 0):
            return TEMPO_FINITO
