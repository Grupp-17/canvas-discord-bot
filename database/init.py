# Init the database

# Internal modules

# Local modules
from canvas.http_requests import *
from .queries import *
from .interactions import *
from utils import get_debug

def init_database():
    conn = create_connection(db_path)

    if conn is not None:
        sql_query(sql_drop_table_courses)
        sql_query(sql_drop_table_announcements)

        if((sql_query(sql_create_table_courses)) and (sql_query(sql_create_table_announcements))):
            return True
        else:
            if(get_debug()):print('Init of tables failed')
            SystemExit()
    else:
        if(get_debug()):print(conn)

        return False
