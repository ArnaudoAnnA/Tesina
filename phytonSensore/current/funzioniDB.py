import sqlite3
import config
#gestire errori


def db_connect(file_path):
    conn = sqlite3.connect(file_path)
    return conn

def get_exercise(db_conn, id_exercise):

    #Marco aggiungi try catch
    cursor = db_conn.cursor()
    query = "SELECT {}, {}, {} FROM exercises WHERE id_ex = {}"
    
    cursor.execute(query.format(config.NAME, config.DESCRIPTION, config.AUDIO, id_exercise))    #dare nomi più significativi nel file config

    row = cursor.fetchone()
    
    return row  #ritorno la riga, nella funzione client me li prendo (è meglio così)


#per testare (da eliminare)
conn = db_connect('brian.db')
get_exercise(conn, 1)
