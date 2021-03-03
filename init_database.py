# Init the database

# Internal modules
from pathlib import Path
import sqlite3
from sqlite3 import Error

# Local modules
from database.queries import *
from canvas.requests import *

# Path is used to create OS independent pathing
db_path = Path('database/main.db')

def create_connection(db_file):
    conn = None

    try:
        conn = sqlite3.connect(db_file)
        print('Connection successful. SQLite3', sqlite3.version)
    except sqlite3.Error as e:
        print(e)
    return conn


def sql_query(conn, query, commit):
    try:
        c = conn.cursor()
        c.execute(query)
        print(query)
        print('Query successful!')

        if commit:
            conn.commit()

    except Error as e:
        print(e)

if __name__ == '__main__':
    conn = create_connection(db_path)

    init_success = False

    if conn is not None:
        sql_query(conn, sql_drop_table, False)
        sql_query(conn, sql_create_table, False)
        init_success = True
    else:
        print(conn)

    if init_success:
        # Get data from request
        data = send_request('courses')

        # Insert answer into database
        sql_query(conn, sql_insert_into(data['name'], data['course_code'], data['created_at']), True)