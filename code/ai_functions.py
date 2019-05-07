# coding=utf-8
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
import sensor_functions
import db_functions
import config 

LENFIFO=config.LENFIFO
CSV_PATH=config.CSV_PATH
AI_PATH=config.AI_PATH
N_ESTIMATORS=config.N_ESTIMATORS
MAX_DEPTH=config.MAX_DEPTH

#function that, given the sensor position, trains and serializes the AI
def saveFitIA(sensorPosition):
    serialized = AI_PATH + sensorPosition + ".pkl" # serialized file path
    header = ['Ax_' + str(i) for i in xrange(1, LENFIFO+1)]+['Ay_' + str(i) for i in xrange(1, LENFIFO+1)]+['Az_' + str(i) for i in xrange(1, LENFIFO+1)]+['Gx_' + str(i) for i in xrange(1, LENFIFO+1)]+['Gy_' + str(i) for i in xrange(1, LENFIFO+1)]+['Gz_' + str(i) for i in xrange(1, LENFIFO+1)]+['movement_class'] # data heading
    data = pd.read_csv(filepath_or_buffer = CSV_PATH + position + '.csv', header=None, index_col=0, names=header) # reading data from csv, indexing the columns
    data = data.sample(frac=1) # data shuffled in order to minimize near rows dependency
    features = [col for col in data.columns.tolist() if col!='movement_class'] # variable containing features indexes (x in our function)
    x_train = data[features].values # x variable of the function (input)
    y_train = data['movement_class'].values # y variable of the function (category)
    rfc = RandomForestClassifier(max_depth=MAX_DEPTH, n_estimators=N_ESTIMATORS, random_state=0) # RandomForest instantiation
    rfc.fit(x_train, y_train) # ai training
    joblib.dump(rfc, serialized) # fit ai serialization
    
#function that, given a row of LENFIFO sensor data, returns the recognized movement class and its percentage of correctness
def movementRecognizer(sensorPosition, movement):
    serialized = AI_PATH + sensorPosition + ".pkl" # serialized file path
    rfc = joblib.load(serialized)
    return rfc.predict_proba(movement)
    
    
    
    
    
    