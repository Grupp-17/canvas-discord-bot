from database.interactions import *
from database.queries import *
from discord_api.commands.subscribe import is_subscribed

def news():
    course_id = create_sql_query_list(sql_query_fetch(sql_select_table_attributes('id', 'courses')))

    for i in course_id: 
        if is_subscribed(i):
            result = "Announcements"
            return result
        else:
            return "No subscribes"