# coding: utf-8

import db_functions as db

test = db.Database()
if(test.conn == None or test.table_exercises == None):
    print ("errore Database()", test)

row = test.table_exercises.get_exercise(1)
if(row==None):
    print("errore get_exercise()", row)

rows = test.table_exercises.get_all_exercises()
if(rows==None):
    print("errore get_all_exercise()", rows)

indexcol = test.table_exercises.get_column_index(test.table_exercises.COLUMN_ID_EXERCISE)
if(indexcol!=0):
    print("errore get_column_index()", indexcol)

max = int(test.table_exercises.get_max_exercise_id())
min = int(test.table_exercises.get_min_exercise_id())
print("rows: ", rows, "\n max id: ", max, "min id: ", min)

bool = test.table_exercises.is_already_present(min)
if(bool==False):
    print("errore is_already_present()", bool)

id = 1
name = test.table_exercises.get_exercise_name(id)
if(name != row[1]):
    print("errore get_exercise_name()", name)

new = max+1
ret = test.table_exercises.add_new_exercise(new, "prova", "prova_test_db_funcitions")
if(ret!=0):
    print("errore add_new_exercise()", ret)
