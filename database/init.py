# Initiation code for the database

# Internal modules
import sys

# Local modules
from .queries import \
    query_drop_table_courses, \
    query_drop_table_announcements, \
    query_create_table_courses, \
    query_create_table_announcements
from .interactions import \
    sql_query, \
    create_connection
from utils import \
    get_config
from log_handler import \
    logger

def init_database():

    # Test connection to database
    conn = create_connection()

    if conn:

        if(get_config('permanent_database')) == False:
            sql_query(query_drop_table_courses)
            sql_query(query_drop_table_announcements)

        if((sql_query(query_create_table_courses)) and (sql_query(query_create_table_announcements))):
            return True
        else:
            logger.critical('Could not initialize database. Shutting down.')
            sys.exit()

