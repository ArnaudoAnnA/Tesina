# coding=utf-8

import sqlite3
import config
#gestire errori

#RISOLVERE PROBLEMA DEL fatchAll() in get_exercises() e get_sensors()


class Database:
    
    NAME = "brian.db"
    PATH = "/home/pi/Downloads/Tesina-master/phytonSensore/current/"  #IMPORTANTE!! specificare sempre il PATH ASSOLUTO 
    
    @staticmethod
    def db_connect():  
        conn = sqlite3.connect(Database.PATH+Database.NAME)
        return conn
    
    

class Table_Exercises:
    TABLENAME = "exercises"
    
    COLUMN_EXID = "ex_id"
    COLUMN_NAME  = "name"
    COLUMN_DESCRIPTION  = "description"
    COLUMN_AUDIO = "audio"
    COLUMN_TIME_SECONDS = "time_seconds"
    
    COLUMNS = [COLUMN_EXID, COLUMN_NAME, COLUMN_DESCRIPTION, COLUMN_AUDIO, TIME_SECONDS]
        
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
            
        return row  #ritorno la riga, nella funzione client me li prendo (è meglio così)
    
    @staticmethod
    def get_allExercises(db_conn):
        try:
            cursor = db_conn.cursor()

            query = "SELECT * FROM {}"
            cursor.execute(query.format(Table_Exercises.TABLENAME))
            #fetchall() method to fetch all rows from the database table
            row = cursor.fetchall()
                           
        except sqlite3.Error as e:
            return "Errore del Database"
        except Exception as e:
            return "Errore: Eccezione nelle query"
                           
        return row  #ritorno tutte le righe, nella funzione client me li prendo

class Table_Sensors:
    TABLENAME = "sensors"
    
    COLUMN_SENSID = "sens_id"
    COLUMN_POSITION= "position"
    COLUMN_PATHFILE = "path_file"
    COLUMN_PATHIAFIT = "pathIA_fit"
    
    COLUMNS = [COLUMN_SENSID, COLUMN_POSITION, COLUMN_PATHFILE, COLUMN_PATHIAFIT]
    
    @staticmethod 
    def get_sensors(db_conn)
        try:
            cursor = db_conn.cursor()
            query = "SELECT * FROM {}"
            cursor.execute(query.format(Table_Sensors.TABLENAME))
            #fetchall() method to fetch all rows from the database table
            row = cursor.fetchall()
            
        except sqlite3.Error as e:
            return "Errore del Database"
        except Exception as e:
            return "Errore: Eccezione nelle query"
                           
        return row  #ritorno tutte le righe, nella funzione client me li prendo
               
    
    
    
    
        
        
