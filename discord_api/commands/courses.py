from database.interactions import *
from database.queries import *
import discord

# TODO Comments

def courses_command(ctx):
    course_names_query = sql_query_fetch(sql_select_table_attributes("name", "courses"))
    course_codes_query = sql_query_fetch(sql_select_table_attributes("course_code", "courses"))
    course_subscribed_query = sql_query_fetch(sql_select_table_attributes("subscribed_to", "courses"))
    id_query = sql_query_fetch(sql_select_table_attributes("id", "courses"))
    
    course_names = []
    course_codes = []
    course_subscribed = []
    id_list = []

    for names, codes, sub, id in zip(course_names_query, course_codes_query, course_subscribed_query, id_query):
        course_names.append(names[0])
        course_codes.append(codes[0])
        course_subscribed.append(sub[0])
        id_list.append(id[0])

    # Embed for displaying courses in discord
    embed = discord.Embed(title='Avaliable courses', 
                        colour=0x98FB98)
    
    embed.set_author(name="CanvasDiscordBot", 
                    icon_url="https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180")
    
    # Add fields in the embed by iterating through the lists
    for name, code, sub, id in zip(course_names, course_codes, course_subscribed, id_list):
        if sub == 1:
            sub = "✓"
        else:
            sub = " "
        embed.add_field(name=str(name) + " " + sub, value=code + " | " + str(id), inline=False)
    return embed