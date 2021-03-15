from database.interactions import *
from database.queries import *
from discord_api.commands.subscribe import is_subscribed
import discord

def announcement(id):
    # Check which context_code id has
    context_code = sql_query_fetchone_result(sql_select_table_attributes_condition("context_code", "announcements", f"id = {id}"))
    course_id = context_code.strip("course_")
    
    if is_subscribed(course_id):
        return print_announcements_embed(context_code)
    else:
        return None

def print_announcements_embed(context_code):

    announcement = create_sql_query_list(sql_query_fetch(sql_select_table_attributes_condition("*", "announcements", f"context_code = '{context_code}'")))

    id = announcement[0]
    title = announcement[1]
    message = announcement[2]
    author = announcement[3]
    context_code = announcement[4]
    posted_at = announcement[5]
    
    embed = discord.Embed(title="Anslag", 
                          description=posted_at, 
                          colour=0x98FB98)
    embed.add_field(name=title, value=message, inline=False)
    return embed