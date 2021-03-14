from database.interactions import *
from database.queries import *
from discord_api.commands.subscribe import is_subscribed
import discord

def announcement(id):
    announcements = create_sql_query_list(sql_query_fetch(sql_select_announcements(id)))
    
    course_id = findCourse(announcements[4])

    if is_subscribed(course_id):
        return print_announcements_embed(announcements)
    else:
        return 0

def findCourse(announcement_context_code):
    course_id = create_sql_query_list(sql_query_fetch(sql_select_table_attributes('id', 'courses')))
    
    for id in course_id:
        if (str(course_id[id]) in announcement_context_code):
            return id
        else:
            return 1

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