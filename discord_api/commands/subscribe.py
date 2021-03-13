from database.interactions import *
from database.queries import *

def subscribe_command(arg):
#   kolla igenom alla kurser, vilka kurser är redan subscribed?
    subscribe_query = sql_query_fetch(sql_select_subscription(arg))

    subscribed = [item for i in subscribe_query for item in i]

    if subscribed[2] == 1:
        message = f"Prenumererar redan på kurs {subscribed[0]}: {subscribed[1]}"
    else:
        message = f"Prenumererar på kurs {subscribed[0]}: {subscribed[1]}"
        # TODO uppdatera subscribed till 1
    return message
