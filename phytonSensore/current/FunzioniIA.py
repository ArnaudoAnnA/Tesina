import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
import funzioniSensori
import funzioniDB
import config 

LENFIFO=config.LENFIFO
N_ESTIMATORS=config.N_ESTIMATORS
MAX_DEPTH=config.MAX_DEPTH

#function that, given the sensor position, trains and serializes the AI
def saveFitAI(sensorPosition):
    
    #retriving the path of the file were the serialized Random Forest has to be saved
    DBconn = funzioniDB.Database.db_connect()
    sensor = funzioniDB.Table_Sensors.get_sensor_from_position(DBconn, sensorPosition)
    index_ia_fit = Table_Sensors.COLUMNS.index(Table_Sensors.COLUMN_PATHIAFIT)
    serialized = sensor[indice_ia_fit] # ".pkl" serialized file path
    
    #retriving the path of the csv file that contains all stored exercises
    index_csv = Table_Sensors.COLUMNS.index(Table_Sensors.COLUMN_PATHCSV)
    csv_path = sensor[index_csv]        # ".csv" 
    
    #retriving data for ia training 
    header = ['Ax_' + str(i) for i in xrange(1, LENFIFO+1)]+['Ay_' + str(i) for i in xrange(1, LENFIFO+1)]+['Az_' + str(i) for i in xrange(1, LENFIFO+1)]+['Gx_' + str(i) for i in xrange(1, LENFIFO+1)]+['Gy_' + str(i) for i in xrange(1, LENFIFO+1)]+['Gz_' + str(i) for i in xrange(1, LENFIFO+1)]+['movement_class'] # data heading
    data = pd.read_csv(csv_path, header=None, index_col=0, names=header) # reading data from csv, indexing the columns
    data = data.sample(frac=1) # data shuffled in order to minimize near rows dependency
    features = [col for col in data.columns.tolist() if col!='movement_class'] # variable containing features indexes (x in our function)
    x_train = data[features].values # x variable of the function (input)
    y_train = data['movement_class'].values # y variable of the function (category)
    
    #ia training
    rfc = RandomForestClassifier(max_depth=MAX_DEPTH, n_estimators=N_ESTIMATORS, random_state=0) # RandomForest instantiation
    rfc.fit(x_train, y_train) # ai training
    joblib.dump(rfc, serialized) # fit ai serialization
    
#function that, given a row of LENFIFO sensor data, returns the recognized movement class and its percentage of correctness
def movementRecognizer(sensorPosition, movement):
    serialized = AI_PATH + sensorPosition + ".pkl" # serialized file path
    rfc = joblib.load(serialized)
    return rfc.predict_proba(movement)
    
    
    
    
    
    