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

# def findCourse(announcement_context_code):
#     courses_id = create_sql_query_list(sql_query_fetch(sql_select_table_attributes('id', 'courses')))

#     id = announcement_context_code.strip("course_")

#     for i in courses_id:
#         if (i == id):
#             return i

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