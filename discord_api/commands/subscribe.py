from database.interactions import *
from database.queries import *

def is_subscribed(course_id):
    subscribe_query = sql_query_fetch(sql_select_subscription(course_id))

    subscribed = [item for i in subscribe_query for item in i]

    if subscribed[2] == 1:
        return True
    else:
        return False

def subscribe_command(arg):
#   kolla igenom alla kurser, vilka kurser är redan subscribed?
    if is_subscribed(arg):
        message = f"Prenumererar redan på kurs {arg}"
    else:
        message = f"Prenumererar på kurs {arg}"
        sql_query(sql_update_subscription(arg, subscribe=True))
    return message


# def subscribe_command(arg):
# #   kolla igenom alla kurser, vilka kurser är redan subscribed?
#     subscribe_query = sql_query_fetch(sql_select_subscription(arg))

#     subscribed = [item for i in subscribe_query for item in i]

#     if subscribed[2] == 1:
#         message = f"Prenumererar redan på kurs {subscribed[0]}: {subscribed[1]}"
#     else:
#         message = f"Prenumererar på kurs {subscribed[0]}: {subscribed[1]}"
#         sql_query(sql_update_subscription(arg, subscribe=True))
#     return message
