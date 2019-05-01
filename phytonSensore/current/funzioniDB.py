# coding=utf-8

import sqlite3
import config
#gestire errori


class Database:
    
    NAME = "brian.db"
    PATH = "/home/pi/Downloads/Tesina-master/phytonSensore/current/"  #IMPORTANTE!! specificare sempre il PATH ASSOLUTO 
    
    
    def db_connect():  
        conn = sqlite3.connect(PATH+NAME)
        return conn
    
    
#IMPORTANTE!! gli id dei vari esercizi devono comporre una serie progressiva di numeri senza NESSUN buco
class Table_Exercises:
    TABLENAME = "exercises"
    
    COLUMN_EXID = "ex_id"
    COLUMN_NAME  = "name"
    COLUMN_DESCRIPTION  = "description"
    COLUMN_AUDIO = "audio"
    COLUMN_TEMPO = "tempo"
    
    COLUMNS = [COLUMN_EXID, COLUMN_NAME, COLUMN_DESCRIPTION, COLUMN_AUDIO, COLUMN_TEMPO]
        
        
    def get_exercise(db_conn, id_exercise):
          
        if(id_exercise < 0):
            return "Errore: Indice inserito non valido"
    
        try:
            cursor = db_conn.cursor()
            query = "SELECT * FROM {} WHERE {} = {}"
            cursor.execute(query.format(Table_Exercises.TABLENAME, Table_Exercises.COLUMN_EXID, id_exercise))   
            row = cursor.fetchone()
            
        except sqlite3.Error as e:
            return "Errore del Database"
        except Exception as e:
            return "Errore: Eccezione nelle query"
            
        return row  #ritorno la riga, nella funzione client me li prendo (è meglio così)
    
    
    def get_allExercise(db_conn){
        try:
            cursor = db_conn.cursor()
            query = "SELECT * FROM {}"
            cursor.execute(query.format(Table_Exercises.TABLENAME)   

            #fetchall() method to fetch all rows from the database table
            row = cursor.fetchall()
                           
        except sqlite3.Error as e:
            return "Errore del Database"
        except Exception as e:
            return "Errore: Eccezione nelle query"
                           
        return row  #ritorno tutte le righe, nella funzione client me li prendo
    
                        
        
        
