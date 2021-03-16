# Managing the announcement command

# Local modules
from utils import html_to_raw

# Third party modules
from database.interactions import *
from database.queries import *
from discord_api.commands.subscribe import is_subscribed
import discord

# Function for receving the announcement and returns an discord embed of it
# if it is subscribed to

def announcement(announcement_id):
    # Get the context_code of the announcement which contains the course id
    context_code = sql_query_fetchone_result(sql_select_table_attributes_condition("context_code", "announcements", f"id = {announcement_id}"))
    
    # Strip the context_code to get only the course id
    course_id = context_code.strip("course_")
    
    # Check if the course of the announcement is subscribed to
    if is_subscribed(course_id):
        return create_announcements_embed(announcement_id, course_id)
    else:
        return None

# Creates the embed for announcements in discord
def create_announcements_embed(announcement_id, course_id):

    # Queries to get all information from the announcements table and the courses table
    announcement = create_sql_query_list(sql_query_fetch(sql_select_table_attributes_condition("*", "announcements", f"id = '{announcement_id}'")))
    course = create_sql_query_list(sql_query_fetch(sql_select_table_attributes_condition("*", "courses", f"id = '{course_id}'")))

    # Declare the information into variables

    # Announcement information
    id = announcement[0]
    title = announcement[1]
    message = announcement[2]
    author = announcement[3]
    context_code = announcement[4]
    posted_at = announcement[5].replace("T", " at ")
    posted_at_formatted = posted_at.replace("Z", "")

    # Parse the text that is recieved in html
    message_raw = html_to_raw(message)

    # Courses information
    course_name = course[1]
    course_code = course[2]
    c_id = course[0]
    
    # Embed layout
    embed = discord.Embed(title="New Announcement 📢", 
                          description=f"Course: {course_id}\n{course_name} | {course_code} \n", 
                          colour=0x98FB98)

    embed.set_author(name="CanvasDiscordBot", 
                    icon_url="https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180")

    embed.add_field(name=title, value=message_raw + "\n\n\n ", inline=False)
    embed.set_footer(text="Posted " + posted_at_formatted + f"\nby {author}")
    return embed