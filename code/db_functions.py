
# coding=utf-8
import sqlite3
import config

#DB connection constants
DB_PATH     = config.DB_PATH
DB_NAME     = config.DB_NAME

#DB main class
class Database:

    #constructor, instances TableExercises
    def __init__(self):  
        self.conn = sqlite3.connect(DB_PATH + DB_NAME)
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
    
    #table columns list
    COLUMNS             = [COLUMN_ID_EXERCISE, COLUMN_NAME, COLUMN_DESCRIPTION, COLUMN_AUDIO]

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
    
    
    def id_already_present(self, id_exercise):
        """return true if there is already an exercise with the id_exercise in the table"""
        bool_already_used = False
        
        row = self.get_exercise(id_exercise)
        
        colindex_id_exercise = self.get_column_index(self.COLUMN_ID_EXERCISE)
        if(row[colindex_id_exercise] == id_exercise):
            bool_already_udes = True
        
        
    def get_all_exercises(self):
        try:
            cursor = self.conn.cursor()
            query = "SELECT * FROM {}"
            cursor.execute(query.format(self.TABLE_NAME))
            rows = list(cursor.fetchall()) #fetchall() method to fetch all rows from the database table
            
        except sqlite3.Error as e:
            return e
        except Exception as e:
            return e
        cursor.close()
        return rows 
        
    def get_column_index(self, column_name):
        return self.COLUMNS.index(column_name) 
    
    def get_maximum_exercise_id(self):

        try:
            cursor = self.conn.cursor()
            query = "SELECT MAX({}) FROM {}"
            cursor.execute(query.format(self.COLUMN_ID_EXERCISE, self.TABLE_NAME))
            row = cursor.fetchone()

        except sqlite3.Error as e:
            return e
        except Exception as e:
            return e

        cursor.close()
        return row  



    def get_minimum_exercise_id(self):

        try:
            cursor = self.conn.cursor()
            query = "SELECT MIN({}) FROM {}"
            cursor.execute(query.format(self.COLUMN_ID_EXERCISE, self.TABLE_NAME))
            row = cursor.fetchone()

        except sqlite3.Error as e:
            return e
        except Exception as e:
            return e
        
        cursor.close()
        return row  



    def get_exercise_name(self, id_exercise):
        if(id_exercise < 0):
            return "Error: index not valid"
        
        try:
            cursor = self.conn.cursor()
            query = "SELECT {} FROM {} WHERE {} = {}"
            cursor.execute(query, self.COLUMN_NAME, self.TABLE_NAME, self.COLUMN_ID_EXERCISE, id_exercise)  
            row = cursor.fetchone()  

        except sqlite3.Error as e:
            return e
        except Exception as e:
            return e
        
        cursor.close()
        return row
    
    
    def add_new_exercise(id_exercise, name, description):
        if(id_exercise < 0):
            return "Error: index not valid"
        
        try:
            cursor = self.conn.cursor()
            query = "INSERT INTO ?(?, ?, ?) VALUES (?, ?, ?)"
            cursor.execute(query, self.TABLE_NAME, self.COLUMN_ID_EXERCISE, self.COLUMN_NAME, self.COLUMN_DESCRIPTION, id_exercise, name, description)  
            
        except sqlite3.Error as e:
            return e
        except Exception as e:
            return e
        
        cursor.close()
        
