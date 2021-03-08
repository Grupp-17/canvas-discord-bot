# Init the database

# Internal modules

# Local modules
from canvas.http_requests import *
from .queries import *
from .interactions import *

def init_database():
    conn = create_connection(db_path)

    # init of database successful?
    init_success = False

    if conn is not None:
        init_success = sql_query(sql_drop_table)
        init_success = sql_query(sql_create_table)

        return True
        
    else:
        print(conn)

        return False
