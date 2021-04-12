# Initiation code for the database

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
    get_debug, \
    get_config

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

