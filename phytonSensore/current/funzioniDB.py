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
    
    

class Table_Exercises:
    TABLENAME = "exercises"
    
    COLUMN_EXID = "ex_id"
    COLUMN_NAME  = "name"
    COLUMN_DESCRIPTION  = "description"
    COLUMN_AUDIO = "audio"
    
    columns = [COLUMN_EXID, COLUMN_NAME, COLUMN_DESCRIPTION, COLUMN_AUDIO]
        
    def get_exercise(db_conn, id_exercise):

        #Marco aggiungi try catch
        cursor = db_conn.cursor()
        
        query = "SELECT * FROM {} WHERE {} = {}"
        
        cursor.execute(query.format(Table_Exercises.TABLENAME, Table_Exercises.COLUMN_EXID, id_exercise))    
     
        row = cursor.fetchone()
        
        return row  #ritorno la riga, nella funzione client me li prendo (è meglio così)
        
        