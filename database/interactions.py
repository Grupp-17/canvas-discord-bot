# Commands for interacting with the database

#internal modules
from database.queries import query_select_table_attributes, query_select_table_attributes_condition
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


def get_course_data(arg):

    data = sql_query_fetchall_result(query_select_table_attributes_condition('*', 'courses', f"{arg}"))

    course_data = {
        'id': f'{data[0]}',
        'name': f'{data[1]}',
        'course_code': f'{data[2]}',
        'start_at': f'{data[3]}',
        'end_at': f'{data[4]}',
        'timestamp': f'{data[5]}',
        'subscribed_to': f'{data[6]}',
        'channel_id': f'{data[7]}'
    }
 
    return course_data


def get_all_courses_data():

    all_data = sql_query_fetchall(query_select_table_attributes('*', 'courses'))

    all_courses_data = []

    for data in all_data:
        data_dict = {
            'id': f'{data[0]}',
            'name': f'{data[1]}',
            'course_code': f'{data[2]}',
            'start_at': f'{data[3]}',
            'end_at': f'{data[4]}',
            'timestamp': f'{data[5]}',
            'subscribed_to': f'{data[6]}',
            'channel_id': f'{data[7]}'
        }

        all_courses_data.append(data_dict)

    return all_courses_data


def get_announcement_data(arg):

    data = sql_query_fetchall_result(query_select_table_attributes_condition('*', 'announcements', f'{arg}'))

    announcement_data = {
        'id': f'{data[0]}',
        'title': f'{data[1]}',
        'message': f'{data[2]}',
        'author': f'{data[3]}',
        'context_code': f'{data[4]}',
        'posted_at': f'{data[5]}',
        'timestamp': f'{data[6]}',
        'sent_discord': f'{data[7]}'
    }
 
    return announcement_data


def get_all_announcements_data():

    all_data = sql_query_fetchall(query_select_table_attributes('*', 'announcements'))

    all_announcements_data = []

    for data in all_data:
        announcement_data = {
            'id': f'{data[0]}',
            'title': f'{data[1]}',
            'message': f'{data[2]}',
            'author': f'{data[3]}',
            'context_code': f'{data[4]}',
            'posted_at': f'{data[5]}',
            'timestamp': f'{data[6]}',
            'sent_discord': f'{data[7]}'
        }

        all_announcements_data.append(announcement_data)
 
    return all_announcements_data

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

def sql_query_fetchall(query):
    try:
        conn = create_connection()
        c = conn.cursor()
        c.execute(query)
        if(get_debug()):
            print(query)
            print('Query successful!')
        
        result = c.fetchall()

        # Return list of query result
        return result

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