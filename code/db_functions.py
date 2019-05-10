# coding=utf-8
import sqlite3
import config

#DB connection constants
DB_PATH     = config.DB_PATH
DB_NAME     = config.DB_NAME

#DB main class
class Database:
    conn            = None
    table_exercises = None

    #constructor, instances TableExercises
    def __init__():  
        self.table_exercises = TableExercises(conn)
        self.conn = sqlite3.connect(DB_PATH+DB_NAME)
    

#DB table exercises class
class TableExercises:

    conn                = None
    
    table_name          = config.TABLE_EXERCISES
    column_id_exercise  = config.EXERCISES_ID_EXERCISE
    column_name         = config.EXERCISES_NAME 
    column_description  = config.EXERCISES_DESCRIPTION
    column_audio        = config.EXERCISES_AUDIO
    
    columns             = [column_id_exercise, column_name, column_description, column_audio]

    #constructor
    def __init__(self, conn):  
        self.conn = conn
   
    #function that, given an exercise id, returns its proprieties
    def get_exercise(self, id_exercise):
        try:
            cursor = self.conn.cursor()
            query = "SELECT * FROM {} WHERE {} = {}"
            if(id_exercise < 0):
                return "Error: index not valid"
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
