'''
USAGE: python mov_rec.py movement_class acquisitionTime
'''
import baal
bus = smbus.SMBus(1)    # or bus = smbus.SMBus(0) for older version boards
#initializing the sensors
baal.MPU_Init(config.Device_Address1)
baal.MPU_Init(config.Device_Address2)