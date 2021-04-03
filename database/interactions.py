# Commands for interacting with the database

#internal modules
import sqlite3
from sqlite3 import Error
from datetime import datetime

# Local modules
from utils import get_debug

# Third party modules
from pathlib import Path

# Path is used to create OS independent pathing
db_path = Path('database/main.db')

def create_connection(): 
    conn = None

    try:
        conn = sqlite3.connect(db_path)
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
        conn = create_connection()
        c = conn.cursor()
        c.execute(query)
        if(get_debug()):
            print(query)
            print('Query successful!')
        return True

    except Error as e:
        if(get_debug()):print(e)
        return False

def sql_query_fetch(query):
    try:
        conn = create_connection()
        c = conn.cursor()
        c.execute(query)
        if(get_debug()):
            print(query)
            print('Query successful!')
        result = c.fetchall()
        return result
       
    except Error as e:
        if(get_debug()):print(e)
        return False

def sql_query_fetchone_result(query):
    try:
        conn = create_connection()
        c = conn.cursor()
        c.execute(query)
        if(get_debug()):
            print(query)
            print('Query successful!')
        
        result = c.fetchone()

        # Return first result only (ignoring ,)
        return result[0]

    except Error as e:
        if(get_debug()):print(e)

def sql_query_fetchall_result(query):
    try:
        conn = create_connection()
        c = conn.cursor()
        c.execute(query)
        if(get_debug()):
            print(query)
            print('Query successful!')
        
        result = c.fetchall()

        # Return list of query result
        return create_sql_query_list(result)

    except Error as e:
        if(get_debug()):print(e)

def sql_query_commit(query):
    try:
        conn = create_connection()
        c = conn.cursor()
        c.execute(query)
        
        conn.commit()

        if(get_debug()):
            print(query)
            print('Query commit successful!')
           
    except Error as e:
        if(get_debug()):print(e)

# Function to set timestamp in database
# TODO Maybe move to utils.py?
def timestamp():
    return datetime.now().strftime('%Y:%m:%dT%I:%M:%S')