# coding=utf-8
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib as jbl
import sensor_functions
import config 
import threading

LENFIFO         = config.LENFIFO
CSV_FILE_PATH   = config.CSV_FILE_PATH
AI_PATH         = config.AI_PATH
N_ESTIMATORS    = config.N_ESTIMATORS
MAX_DEPTH       = config.MAX_DEPTH
HEADER_FEATURES = config.HEADER_FEATURES
HEADER          = config.HEADER
ID_EXERCISE     = config.ID_EXERCISE

    
class TheBrain(threading.Thread):

    #RandomForest instantiation
    rfc                 = RandomForestClassifier(max_depth=MAX_DEPTH, n_estimators=N_ESTIMATORS, random_state=0) 
    sensor_position     = None
    serialized_path     = None
    observer            = audio_feedback_esercizio.AudioFeedBackEsercizio

    #constructor
    def __init__(self, sensor_position):
        self.sensor_position = sensor_position
        self.serialized_path = AI_PATH + sensor_position + ".pkl"
        
    #----RUN----------------------------------------------------------------------------------------------    
    #function called when an IA thread starts
    #calculates the percentage of correctNess
    def run(self, id_exercise, semaphore):
        while(semaphore.is_unLocked()):    #thread will be interrupted by the cuntdown of the timer
            #CODICE CHE RICAVA LA PERCENTUALE DI CORRETTEZZA CON CUI VIENE ESEGUITO L'ESERCIZIO CORRISPONDENTE A ID_EXERCISE
            observer.ia_result_notify(IAresult)
    #---------------------------------------------------------------------------------------------------------
            
    #function that trains the AI using an input csv 
    def fit_from_csv(self):
        #reading data from csv, indexing the columns
        data = pd.read_csv(filepath_or_buffer = CSV_FILE_PATH + self.sensor_position + '.csv', header=None, names=HEADER) 
        self.fit(data)


    #function that trains the AI
    def fit(self, data):
        #data shuffled in order to minimize near rows dependency
        data = data.sample(frac=1) 
        #variable containing features indexes (x in our function)
        features = [col for col in data.columns.tolist() if col != ID_EXERCISE] 
        #x variable of the function (input)
        x_train = data[features].values
        #y variable of the function (category) 
        y_train = data[ID_EXERCISE].values 
        #ai training
        self.rfc.fit(x_train, y_train) 

    #function that serializes the object
    def serialize(self):
        #fit ai serialization
        jbl.dump(self.rfc, self.serialized_path) 

    #function that, given the sensor position, trains and serializes the AI
    def save_fit_ai(self):
        self.fit_from_csv()
        self.serialize()

    #function that deserializes the object
    def deserialize(self):
        self.rfc = jbl.load(self.serialized_path)

    #function that, given a row of LENFIFO sensor data, returns the recognized movement class and the percentage of correctness of all possible movements
    def movement_recognizer(self, movement):
        df_movement = pd.DataFrame(data= [movement], columns = HEADER_FEATURES)
        predicted_movement = self.rfc.predict(df_movement)
        predicted_probability = self.rfc.predict_proba(df_movement)
        return (predicted_movement[0], predicted_probability[0])
