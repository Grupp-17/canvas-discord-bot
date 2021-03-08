# Managing the database

#internal modules
import sqlite3
from sqlite3 import Error
from pathlib import Path

# Path is used to create OS independent pathing
db_path = Path('database/main.db')

def create_connection(db_file):
    conn = None

    try:
        conn = sqlite3.connect(db_file)
        print('Connection successful. SQLite3', sqlite3.version)
    except Error as e:
        print(e)
    return conn

def sql_query(query):
    try:
        conn = create_connection(db_path)

        c = conn.cursor()
        c.execute(query)
        print(query)
        print('Query successful!')

        conn.close()

    except Error as e:
        print(e)


def sql_query_commit(query):
    try:
        conn = create_connection(db_path)

        c = conn.cursor()
        c.execute(query)
        
        conn.commit()

        print(query)
        print('Query commit successful!')

        conn.close()
           
    except Error as e:
        print(e)
