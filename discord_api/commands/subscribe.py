from database.interactions import *
from database.queries import *
import discord

# TODO Comments

def is_subscribed(course_id):
    subscribed = sql_query_fetchone_result(sql_select_table_attributes_condition("subscribed_to", "courses", f"id = {course_id}"))

    if subscribed == 1:
        return True
    else:
        return False

def subscribe_command(arg):

    course_id = create_sql_query_list(sql_query_fetch(sql_select_table_attributes("id", "courses")))

    for i in course_id:
        if (i == arg):
            embed = discord.Embed(colour=0x98FB98)
            embed.set_author(name="CanvasDiscordBot", 
                            icon_url="https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180")
            if is_subscribed(arg):
                embed.add_field(name=f"Subscription on course {arg} already satisfied", value="No subscription added!")
            else:
                embed.add_field(name=f"Subscribing on course {arg}", value="Subscription added!")
                sql_query_commit(sql_update_subscription(arg, "1"))
                
                # TODO Remove checks or create suitable debugging message
                #check = sql_query_fetchone_result(sql_select_table_attributes_condition("subscribed_to", "courses", f"id = {arg}"))
                #print(check)
            return embed
        else:
            embed = discord.Embed(colour=0x98FB98)
            embed.set_author(name="CanvasDiscordBot", 
                            icon_url="https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180")
            embed.add_field(name=f"Course '{arg}' does not exist", value="No subscription added!")
            return embed
