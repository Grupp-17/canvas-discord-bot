# Managing the announcement command

# Local modules
from utils import html_to_raw
from database.interactions import *
from database.queries import *
from .subscribe import is_subscribed

# Third party modules
import discord

# Function for receving the announcement and returns an discord embed of it
# if it is subscribed to
def announcement(announcement_id):
    # Get the context_code of the announcement which contains the course id
    
    announcement_data = get_announcement_data(f"id = '{announcement_id}'")

    if(announcement_data):

        context_code = announcement_data.get("context_code")

        # Strip the context_code to get only the course id
        course_id = context_code.strip("course_")
        
        # Check if the course of the announcement is subscribed to
        if is_subscribed(course_id):
            return create_announcement_embed(announcement_id, course_id)
        else:
            return None

# Creates the embed for announcements in discord
def create_announcement_embed(announcement_id, course_id):

    # Queries to get all information from the announcements table and the courses table
    announcement_data = get_announcement_data(f"id = '{announcement_id}'")
    course_data = get_course_data(f"id = '{course_id}'")

    # Declare the information into variables

    # Announcement information
    id = announcement_data.get("id")
    title = announcement_data.get("title")
    message = announcement_data.get("message")
    author = announcement_data.get("author")
    context_code = announcement_data.get("context_code")
    posted_at = announcement_data.get("posted_at").replace("T", " at ")
    posted_at_formatted = posted_at.replace("Z", "")

    # Parse the text that is recieved in html
    message_raw = html_to_raw(message)

    # Courses information
    course_name = course_data.get("name")
    course_code = course_data.get("course_code")
    c_id = course_data.get("id")
    
    # Embed layout
    embed = discord.Embed(title="New Announcement 📢", 
                          description=f"Course: {course_id}\n{course_name} | {course_code} \n", 
                          colour=0x98FB98)

    embed.set_author(name="CanvasDiscordBot", 
                    icon_url="https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180")

    embed.add_field(name=title, value=message_raw + "\n\n\n ", inline=False)
    embed.set_footer(text="Posted " + posted_at_formatted + f"\nby {author}")
    return embed