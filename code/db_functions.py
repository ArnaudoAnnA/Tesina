# coding=utf-8

import sqlite3
import config

HOME_PATH=config.HOME_PATH
#error handling


class Database:
    
    NAME = "brian.db"
    PATH = HOME_PATH+"files/db/"  #IMPORTANT, always use abs path! 
    
    @staticmethod
    def db_connect():  
        conn = sqlite3.connect(Database.PATH+Database.NAME)
        return conn
    
    

class table_exercises:
    TABLENAME = "exercises"
    
    COLUMN_EX_COD = "ex_cod"
    COLUMN_NAME  = "name"
    COLUMN_DESCRIPTION  = "description"
    COLUMN_AUDIO = "audio"
    COLUMN_TIME_SECONDS = "time_seconds"
    
    COLUMNS = [COLUMN_EX_COD, COLUMN_NAME, COLUMN_DESCRIPTION, COLUMN_AUDIO, COLUMN_TIME_SECONDS]

    @staticmethod    
    def get_exercise(db_conn, id_exercise):
        try:
            cursor = db_conn.cursor()
            query = "SELECT * FROM {} WHERE {} = {}"
            if(id_exercise < 0):
                return "Errore: Indice inserito non valido"
            cursor.execute(query.format(Table_Exercises.TABLENAME, Table_Exercises.COLUMN_EXID, id_exercise))   
            row = cursor.fetchone()  
        except sqlite3.Error as e:
            return "Errore del Database"
        except Exception as e:
            return "Errore: Eccezione nelle query"
        return row
        
    @staticmethod
    def get_allExercises(db_conn):
        try:
            cursor = db_conn.cursor()
            query = "SELECT * FROM {}"
            cursor.execute(query.format(Table_Exercises.TABLENAME))
            #fetchall() method to fetch all rows from the database table
            row = list(cursor.fetchall())
        except sqlite3.Error as e:
            return "Errore del Database"
        except Exception as e:
            return "Errore: Eccezione nelle query"
        return row

class Table_Sensors:
    TABLENAME = "sensors"
    
    COLUMN_SENS_COD = "sens_cod"
    COLUMN_POSITION= "position"
    COLUMN_PATH_CSV = "path_csv"
    COLUMN_PATHIA_FIT = "pathIA_fit"
    
    COLUMNS = [COLUMN_SENS_COD, COLUMN_POSITION, COLUMN_PATH_CSV, COLUMN_PATHIA_FIT]
    
    #possible values of attribute "position"
    SENSORPOSITION_LEGSX = "legsx"
    SENSORPOSITION_LEGDX = "legdx"
    SENSORPOSITION_ARMSX = "armsx"
    SENSORPOSITION_ARMDX = "armdx"
    
    @staticmethod
    def get_allSensors(db_conn):
        try:
            cursor = db_conn.cursor()
            query = "SELECT * FROM {}"
            cursor.execute(query.format(Table_Sensors.TABLENAME))
            #fetchall() method to fetch all rows from the database table
            rows = cursor.fetchall()
        except sqlite3.Error as e:
            return "Errore del Database"
        except Exception as e:
            return "Errore: Eccezione nelle query"
        return rows
    
    @staticmethod
    def get_sensorFromPosition(db_conn, sensorPosition):
        try:
            cursor = db_conn.cursor()
            query = "SELECT * FROM {} WHERE {} = {}"
            cursor.execute(query.format(Table_Sensors.TABLENAME, Table_Sensors.COLUMN_POSITION, sensorPosition))
            #fetchall() method to fetch all rows from the database table
            row = cursor.fetchone()
        except sqlite3.Error as e:
            return "Errore del Database"
        except Exception as e:
            return "Errore: Eccezione nelle query"
                           
        return row
    
    

conn = Database.db_connect()
sensors = Table_Sensors.get_sensorFromPosition(conn, Table_Sensors.SENSORPOSITION_LEGSX)
print (sensors)
        