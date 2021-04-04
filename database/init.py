# Initiation code for the database

# Internal modules

# Local modules
from canvas.http_requests import *
from .queries import *
from .interactions import sql_query, create_connection
from utils import get_debug, get_config

# Third party modules

def init_database():

    conn = create_connection()

    if conn is not None:

        if(get_config('permanent_database')) == False:
            sql_query(query_drop_table_courses)
            sql_query(query_drop_table_announcements)

        # TODO Comment
        if((sql_query(query_create_table_courses)) and (sql_query(query_create_table_announcements))):
            return True
        else:
            if(get_debug()):print('Init of tables failed')
            SystemExit()
    else:
        if(get_debug()):print(conn)

        return False

