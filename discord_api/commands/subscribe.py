from database.interactions import *
from database.queries import *
import discord

def is_subscribed(course_id):
    subscribed = create_sql_query_list(sql_query_fetch(sql_select_subscription(course_id)))

    if subscribed[2] == "1":
        return True
    else:
        return False

def subscribe_command(arg):
#   kolla igenom alla kurser, vilka kurser är redan subscribed?

    # TODO Sanitize imput from user

    embed = discord.Embed(title='Prenumerationer', colour=0x98FB98)
    embed.set_author(name="CanvasDiscordBot", 
                     icon_url="https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180")
    if is_subscribed(arg):
        embed.add_field(name=f"Prenumererar redan på kurs {arg}", value="Ingen ny prenumeration tillagd")
    else:
        embed.add_field(name=f"Prenumererar nu på kurs {arg}", value="Kursen lades till")
        sql_query(sql_update_subscription(arg, "1"))
    return embed


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
