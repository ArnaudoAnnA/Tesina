# coding=utf-8
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
import sensor_functions
import config 

LENFIFO=config.LENFIFO
CSV_PATH=config.CSV_PATH
AI_PATH=config.HOME_PATH+"/files/pkl/"
#function that, given the sensor position, trains and serializes the AI

#TODO: DEBUG, COMMENTS
    
class AI:

	rfc = None
	n_estimators = 0
	max_depth = 0
	header_features = None
	header = None

	def __init__(self):
        self.header_features = ['Ax_' + str(i) for i in xrange(1, LENFIFO+1)]+['Ay_' + str(i) for i in xrange(1, LENFIFO+1)]+['Az_' + str(i) for i in xrange(1, LENFIFO+1)]+['Gx_' + str(i) for i in xrange(1, LENFIFO+1)]+['Gy_' + str(i) for i in xrange(1, LENFIFO+1)]+['Gz_' + str(i) for i in xrange(1, LENFIFO+1)] # data heading
		self.header = header_features+['movement_class']
		self.rfc = RandomForestClassifier(max_depth=self.max_depth, n_estimators=self.n_estimators, random_state=0) # RandomForest instantiation

	def fit_from_csv(self, sensor_position):
		data = pd.read_csv(filepath_or_buffer = CSV_PATH + sensor_position + '.csv', header=None, names=self.header) # reading data from csv, indexing the columns
		self.fit(self, sensor_position, data)
   		

	def fit(self, sensor_position, data):
		data = data.sample(frac=1) # data shuffled in order to minimize near rows dependency
   		features = [col for col in data.columns.tolist() if col!='movement_class'] # variable containing features indexes (x in our function)
  		x_train = data[features].values # x variable of the function (input)
  		y_train = data['movement_class'].values # y variable of the function (category)
		self.rfc.fit(x_train, y_train) # ai training
    
    def serialize(self):
    	serialized = AI_PATH + sensor_position + ".pkl" # serialized file path
   		joblib.dump(self.rfc, serialized) # fit ai serialization

    def save_fit_ai(self, sensor_position):
    	self.fit_from_csv(self, sensor_position)
    	self.serialize()
   	
   	def deserialize(self, sensor_position):
   		df_movement = pd.DataFrame(data= [movement], columns = self.header_features)
    	serialized = AI_PATH + sensor_position + ".pkl" # serialized file path
    	self.rfc = joblib.load(serialized)

    
	#function that, given a row of LENFIFO sensor data, returns the recognized movement class and its percentage of correctness
	def movement_recognizer(self, movement):
    	return (self.rfc.predict(df_movement), self.rfc.predict_proba(df_movement))
    