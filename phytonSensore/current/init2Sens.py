'''
USAGE: python mov_rec.py movement_class acquisitionTime
'''
import baal
import config
#initializing the sensors
baal.MPU_Init(config.Device_Address1)
baal.MPU_Init(config.Device_Address2)