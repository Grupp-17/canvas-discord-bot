# Courses command

# Local modules
from database.interactions import *
from database.queries import *

# Third party modules
import discord

def courses_command(ctx):

    # Queries to get lists containing information about all courses
    course_names = create_sql_query_list(sql_query_fetch(sql_select_table_attributes("name", "courses")))
    course_codes = create_sql_query_list(sql_query_fetch(sql_select_table_attributes("course_code", "courses")))
    course_subscribed_to = create_sql_query_list(sql_query_fetch(sql_select_table_attributes("subscribed_to", "courses")))
    id_list = create_sql_query_list(sql_query_fetch(sql_select_table_attributes("id", "courses")))

    # Embed for displaying all availible courses in discord
    embed = discord.Embed(title='Avaliable courses', 
                        colour=0x98FB98)
    
    embed.set_author(name="CanvasDiscordBot", 
                    icon_url="https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180")
    
    # Adding the fields in the embed by iterating through the lists
    for name, code, sub, id in zip(course_names, course_codes, course_subscribed_to, id_list):
        if sub == 1:
            sub = "🔔"
        else:
            sub = " "
        embed.add_field(name=str(name) + " " + sub, value=code + " | " + str(id), inline=False)
    return embed