from database.interactions import *
from database.queries import *
from discord_api.commands.subscribe import is_subscribed
import discord

def announcement(id):
    # Check which context_code id has
    context_code = sql_query_fetchone_result(sql_select_table_attributes_condition("context_code", "announcements", f"id == {id}"))
    course_id = context_code.strip("course_")
    
    if is_subscribed(course_id):
        return print_announcements_embed(context_code)
    else:
        return None

def print_announcements_embed(announcements):
    id = announcements[0]
    title = announcements[1]
    message = announcements[2]
    author = announcements[3]
    context_code = announcements[4]
    posted_at = announcements[5]
    
    embed = discord.Embed(title="Anslag", 
                          description=posted_at, 
                          colour=0x98FB98)
    embed.add_field(name=title, value=message, inline=False)
    return embed