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
    def __init__(self):  
        self.conn = sqlite3.connect(DB_PATH+DB_NAME)
        self.table_exercises = TableExercises(self.conn)
    

#DB table exercises class
class TableExercises:

    #connection
    conn                = None
    #table constants
    TABLE_NAME          = "exercises"
    COLUMN_ID_EXERCISE  = "id_exercise"
    COLUMN_NAME         = "name"
    COLUMN_DESCRIPTION  = "description"
    COLUMN_AUDIO        = "audio"
    #table columns list
    columns             = [COLUMN_ID_EXERCISE, COLUMN_NAME, COLUMN_DESCRIPTION, COLUMN_AUDIO]

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
            cursor.execute(query.format(self.TABLE_NAME, self.COLUMN_ID_EXERCISE, id_exercise))   
            row = cursor.fetchone()  
            
        except sqlite3.Error as e:
            return e
        except Exception as e:
            return e
            cursor.close()
        return row
        
    def get_all_exercises(self):
        try:
            cursor = self.conn.cursor()
            query = "SELECT * FROM {}"
            cursor.execute(query.format(self.TABLE_NAME))
            row = list(cursor.fetchall()) #fetchall() method to fetch all rows from the database table
            
        except sqlite3.Error as e:
            return e
        except Exception as e:
            return e
        cursor.close()
        return row   
        
    def get_column_index(self, column_name):
        return self.columns.index(column_name)
        return row    