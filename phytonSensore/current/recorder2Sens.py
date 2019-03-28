'''
USAGE: python mov_rec.py movement_class acquisitionTime
'''
import baal

#Arguments:
#the number of the exercise (keeping in mind the recording of error datasets)
movement_class = sys.argv[1]
#the number of the seconds to record
acquisitionTime = sys.argv[2]

#the integer representing the number of instants to record
recordings = int(acquisitionTime*ACQUIRATE)
#initializing the number of recordings recorded
times = 0
#opening the file writer in order to save the dataset in a csv file named like the exercise
csvfile = open(movementsDictionary.name[movement_class]+'.csv', 'ab')
writer = csv.writer(csvfile)
#creating the lists that will become FIFO
sensorFifo1=[]
sensorFifo2=[]
#initializing the FIFO
baal.init_Fifo(LENFIFO, sensorFifo1, AUTH)
baal.init_Fifo(LENFIFO, sensorFifo2, AUTH)
#creating the sensor lists
sensor1=[0]*LENFIFO
sensor2=[0]*LENFIFO
#loop that runs for acquisitionTime time in seconds
for x in range(0, recordings):
	#reading the data from the sensors
	baal.read_sensor_data(sensor1, Device_Address1)
	baal.read_sensor_data(sensor2, Device_Address2)
	#parsing the data in an useful format
	baal.parse_sensor_data(sensor1)
	baal.parse_sensor_data(sensor2)
	#adding the sensor data to the head of the FIFO, automatically deleting the one in the tail
	baal.append_sensor_data(sensorFifo1, sensor1)
	baal.append_sensor_data(sensorFifo2, sensor2)
	#writing the fifo if it has the correct overlap or is the last recording
	if times%(LENFIFO-OVERLAP)==0 or times=recordings-1 :
		writer.writerow(list(sensorFifo1) + list(sensorFifo2) + [movement_class])
	#setting next instant
	times=times+1
	time.sleep(acquisitionRate)
close(csvfile)