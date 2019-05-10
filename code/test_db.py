#test
import db_functions as dbf 
import config as c

db = dbf.Database()
print db.table_exercises.get_all_exercises()
print db.table_exercises.get_exercise(1)
print db.table_exercises.get_exercise(2)
print db.table_exercises.get_exercise(3)