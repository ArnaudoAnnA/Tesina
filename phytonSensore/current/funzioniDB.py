@staticmethod# coding=utf-8

import sqlite3
import config
#gestire errori


class Database:
    
    NAME = "brian.db"
    PATH = "/home/pi/Downloads/Tesina-master/phytonSensore/current/"  #IMPORTANTE!! specificare sempre il PATH ASSOLUTO 
    
    @staticmethod
    def db_connect():  
        conn = sqlite3.connect(PATH+NAME)
        return conn
    
    

class Table_Exercises:
    TABLENAME = "exercises"
    
    COLUMN_EXID = "ex_id"
    COLUMN_NAME  = "name"
    COLUMN_DESCRIPTION  = "description"
    COLUMN_AUDIO = "audio"
    COLUMN_TEMPO = "tempo"
    
    COLUMNS = [COLUMN_EXID, COLUMN_NAME, COLUMN_DESCRIPTION, COLUMN_AUDIO]
        
    @staticmethod    
    def get_exercise(db_conn, id_exercise):
           
        #Marco aggiungi try catch
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
    def get_allExercise(db_conn):
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
    
        
        
