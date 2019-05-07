# coding=utf-8
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
import sensor_functions
import config 

LENFIFO=config.LENFIFO
CSV_PATH=config.CSV_PATH

header_features = ['Ax_' + str(i) for i in xrange(1, LENFIFO+1)]+['Ay_' + str(i) for i in xrange(1, LENFIFO+1)]+['Az_' + str(i) for i in xrange(1, LENFIFO+1)]+['Gx_' + str(i) for i in xrange(1, LENFIFO+1)]+['Gy_' + str(i) for i in xrange(1, LENFIFO+1)]+['Gz_' + str(i) for i in xrange(1, LENFIFO+1)] # data heading
header = header_features+['movement_class']
AI_PATH=config.HOME_PATH+"/files/pkl/"
N_ESTIMATORS = 100
MAX_DEPTH = 3

#function that, given the sensor position, trains and serializes the AI
def save_fit_ai(sensor_position):
    serialized = AI_PATH + sensor_position + ".pkl" # serialized file path
    data = pd.read_csv(filepath_or_buffer = CSV_PATH + sensor_position + '.csv', header=None, names=header) # reading data from csv, indexing the columns
    data = data.sample(frac=1) # data shuffled in order to minimize near rows dependency
    features = [col for col in data.columns.tolist() if col!='movement_class'] # variable containing features indexes (x in our function)
    x_train = data[features].values # x variable of the function (input)
    y_train = data['movement_class'].values # y variable of the function (category)
    rfc = RandomForestClassifier(max_depth=MAX_DEPTH, n_estimators=N_ESTIMATORS, random_state=0) # RandomForest instantiation
    rfc.fit(x_train, y_train) # ai training
    joblib.dump(rfc, serialized) # fit ai serialization
    
#function that, given a row of LENFIFO sensor data, returns the recognized movement class and its percentage of correctness
def movement_recognizer(sensor_position, movement):
    df_movement = pd.DataFrame(data= [movement], columns = header_features)
    serialized = AI_PATH + sensor_position + ".pkl" # serialized file path
    rfc = joblib.load(serialized)
    return rfc.predict_proba(df_movement)
    
    
    
    
    
    