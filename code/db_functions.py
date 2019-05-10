# coding=utf-8
import sqlite3
import config

#DB connection constants
DB_PATH     = config.DB_PATH
DB_NAME     = config.DB_NAME

#DB main class
class Database:

    #constructor, instances TableExercises
    def __init__(): 
        self.conn = sqlite3.connect(DB_PATH+DB_NAME)
        self.table_exercises = TableExercises(self.conn)
        
    

#DB table exercises class
class TableExercises:
    
    TABLE_NAME          = config.TABLE_EXERCISES
    COLUMN_ID_EXERCISE  = config.EXERCISES_ID_EXERCISE
    COLUMN_NAME         = config.EXERCISES_NAME 
    COLUMN_DESCRIPTION  = config.EXERCISES_DESCRIPTION
    COLUMN_AUDIO        = config.EXERCISES_AUDIO
    
    COLUMNS             = [COLUMN_ID_EXERCISE, COLUMN_NAME , COLUMN_DESCRIPTION, COLUMN_AUDIO]

    #constructor
    def __init__(self, conn):  
        self.conn = conn
   
    #function that, given an exercise id, returns its proprieties
    def get_exercise(self, id_exercise):
        if(id_exercise < 0):
                return "Error: index not valid"
        
        try:
            cursor = self.conn.cursor()
            query = "SELECT * FROM {} WHERE {} = {}"
            cursor.execute(query.format(self.table_name, self.column_id_exercise, id_exercise))   
            row = cursor.fetchone()  
            
        except sqlite3.Error as e:
            return "Error: sqlite3 error"
        except Exception as e:
            return "Error: query not valid"
        
        cursor.close()
        return row
    
        
    def get_all_exercises(self):
        try:
            cursor = self.conn.cursor()
            query = "SELECT * FROM {}"
            cursor.execute(query.format(Table_Exercises.table_name))
            row = list(cursor.fetchall()) #fetchall() method to fetch all rows from the database table
            
        except sqlite3.Error as e:
            return "Error: sqlite3 error"
        except Exception as e:
            return "Error: query not valid"
        
        cursor.close()
        return row   
    
    
    def get_column_index(self, column_name):
        return COLUMNS.index(column_name)
