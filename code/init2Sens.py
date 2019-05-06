import funzioniSensori
import config

#initializing the sensors

funzioniSensori.MPU_Init(config.Device_Address1)
funzioniSensori.MPU_Init(config.Device_Address2)