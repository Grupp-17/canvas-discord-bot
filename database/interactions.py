# Commands for interacting with the database

#internal modules
import sqlite3
from sqlite3 import Error
from pathlib import Path
from datetime import datetime

# Local constants
from utils import get_debug

# Path is used to create OS independent pathing
db_path = Path('database/main.db')

def create_connection(db_file): 
    conn = None

    try:
        conn = sqlite3.connect(db_file)
        if(get_debug()):print('Connection successful. SQLite3', sqlite3.version)
    except Error as e:
        if(get_debug()):print(e)
    return conn


# Create a clean list of SQLite output
def create_sql_query_list(data):
    result = []

    for i in range(len(data)):
        for f in range(len(data[i])):
            result.append(data[i][f])

    return result

def sql_query(query):
    try:
        conn = create_connection(db_path)

        c = conn.cursor()
        c.execute(query)
        if(get_debug()):
            print(query)
            print('Query successful!')
        conn.close()
        return True

    except Error as e:
        if(get_debug()):print(e)
        return False

def sql_query_fetch(query):
    try:
        conn = create_connection(db_path)

        c = conn.cursor()
        c.execute(query)
        if(get_debug()):
            print(query)
            print('Query successful!')
        result = c.fetchall()
        conn.close()
        return result
       
    except Error as e:
        if(get_debug()):print(e)
        return False

def sql_query_fetchone_result(query):
    try:
        conn = create_connection(db_path)

        c = conn.cursor()
        c.execute(query)
        if(get_debug()):
            print(query)
            print('Query successful!')
        
        result = c.fetchone()

        conn.close()

        # Return first result only (ignoring ,)
        return result[0]

    except Error as e:
        if(get_debug()):print(e)

def sql_query_fetchall_result(query):
    try:
        conn = create_connection(db_path)

        c = conn.cursor()
        c.execute(query)
        if(get_debug()):
            print(query)
            print('Query successful!')
        
        result = c.fetchall()

        conn.close()

        # Return list of query result
        return create_sql_query_list(result)

    except Error as e:
        if(get_debug()):print(e)

def sql_query_commit(query):
    try:
        conn = create_connection(db_path)

        c = conn.cursor()
        c.execute(query)
        
        conn.commit()

        if(get_debug()):
            print(query)
            print('Query commit successful!')

        conn.close()
           
    except Error as e:
        if(get_debug()):print(e)

# Function to set timestamp in database
def timestamp():
    return datetime.now().strftime('%Y:%m:%dT%I:%M:%S')