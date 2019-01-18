# Tesina
DESCRIZIONE: tuta con sensori alle estemità delle articolazioni che permette il riconoscimnto del movimento eseguito. L'obiettivo è quello di controllare che l'esercizio (sportivo) venga eseguito correttamente. 

# tecnologie utilizzate
- raspberry Pi, 
- (eventuale) rete neurale per rendere più veloce il riconoscimento dei movimenti, 
- sensore accellerometro e giroscopio tre assi (MPU-6050 https://www.invensense.com/products/motion-tracking/6-axis/mpu-6050/).
- (eventuale) interfaccia audio
- java per interfaccia desktop

# dettagli implementazione
Il prototipo realizzato riguarderà un pantalone da corsa con tre sensori MPU-6050 in prossimità dei seguenti punti del corpo:
  - caviglia
  - ginocchio
  - anca
I tre sensori sono collegati ad un Raspberry Pi posizionato in un marsupio legato in vita.
La scheda Raspberry è collegata ad una antenna grazie alla quale trasmette i dati rilevati dai sensori ad un computer.
All'interno del computer avviene il riconoscimento o la memorizzazione dei movimenti (a seconda della modalità selezionata tramite interfaccia desktop). La memorizzazione dei movimenti è necessaria, in una prima fase, per memorizzare la serie di movimenti che poi verrà confrontata con i movimenti percepiti in modalità "riconoscimento".

Una volta realizzato il prototipo per una gamba, eventualmente si potrebbe procedere con la seconda gamba, che sarà identica alla prima ma con un controllo di "simmetricità". 
