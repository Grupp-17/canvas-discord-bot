# Initiation code for the database

# Internal modules

# Local modules
from canvas.http_requests import *
from .queries import *
from .interactions import sql_query, create_connection
from utils import get_debug

# Third party modules

def init_database():

    conn = create_connection()

    if conn is not None:

        # Create cmd line argument for dropping tables
        # TODO We should set an option to drop tables or not in  config.json
        sql_query(sql_drop_table_courses)
        sql_query(sql_drop_table_announcements)

        # TODO Comment
        if((sql_query(sql_create_table_courses)) and (sql_query(sql_create_table_announcements))):
            return True
        else:
            if(get_debug()):print('Init of tables failed')
            SystemExit()
    else:
        if(get_debug()):print(conn)

        return False

