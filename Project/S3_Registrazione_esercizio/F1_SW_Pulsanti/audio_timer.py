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
import output_per_test as audioInterface


class Timer:
    timer = 0

    def __init__(self, valoreIniziale):
        self.timer = valoreIniziale


    def impostaTimer(self, nuovo):
        self.timer = nuovo
        return Timer_changed_listener.notify(self.timer)

    # --------------------------------------------------------------------------------------------------------------------------------------
    def incrementaTimer(self, incremento):
        return self.impostaTimer(self.timer + incremento)

    #------------------------------------------------------------------------------------------------------------------------------------
    def audio_conto_alla_rovescia(self):
        global timer
        while self.incrementaTimer(-1) != TEMPO_FINITO:
            time.sleep(1)  # aspetto un secondo

    # --------------------------------------------------------------------------------------------------------------------------------------------------




# --------------------------------------------------------------------------------------------------------------------------------------------------

class Timer_changed_listener:

    @staticmethod
    def notify(timer):  # metodo statico.
        # viene evocato ogni volta che il numero del timer cambia
        # da in output il nuovo valore del timer.
        # se il nuovo valore è 0, restituisce TEMPO_FINITO, che può essere ignorato o meno a seconda di dove viene richiamato il metodo
        audioInterface.output_audio(timer)
        if (timer == 0):
            return TEMPO_FINITO