from database.interactions import *
from database.queries import *
import discord

def is_subscribed(course_id):
    subscribed = sql_query_fetchone_result(sql_select_table_attributes_condition("subscribed_to", "courses", f"id = {course_id}"))

    if subscribed == "1":
        return True
    else:
        return False

def subscribe_command(arg):

    embed = discord.Embed(title='Prenumerationer', colour=0x98FB98)
    embed.set_author(name="CanvasDiscordBot", 
                     icon_url="https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180")
    if is_subscribed(arg):
        embed.add_field(name=f"Prenumererar redan på kurs {arg}", value="Ingen ny prenumeration tillagd")
    else:
        embed.add_field(name=f"Prenumererar nu på kurs {arg}", value="Kursen lades till")
        sql_query(sql_update_subscription(arg, "1"))
    return embed
