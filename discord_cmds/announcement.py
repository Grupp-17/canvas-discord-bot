# Managing the announcement command

# Local modules
from utils import html_to_raw
from database.interactions import *
from database.queries import *

# Third party modules
import discord

def get_subscribed_courses_data():
    
    courses_data = get_all_courses_data()

    subscribed_courses_data = []
    
    for course in courses_data:

        # Check if subscribed and channel is set
        if(course.get('subscribed_to') == '1') and (course.get('channel_id') != '1'):

            subscribed_courses_data.append(course)

    return subscribed_courses_data

def get_unsent_announcements_data():
    
    announcement_data = get_all_announcements_data()

    unsent_announcements_data = []

    for announcement in announcement_data:
        
        # Check if not sent and if channel is set
        if(announcement.get('sent_discord') == '0'):

            unsent_announcements_data.append(announcement)

    return unsent_announcements_data


def join_courses_with_announcement_data(subscribed_courses_data, unsent_announcements_data):
    
    new_unsent_announcements_data = []

    for course_data in subscribed_courses_data:
        for announcement_data in unsent_announcements_data:
            context_code = announcement_data.get("context_code")

            # Checks that the join is done at the correct place
            if(context_code.strip('course_')) == (course_data.get('id')):
                
                # Add all needed data to dictionary from courses
                announcement_data['channel_id'] = course_data.get('channel_id')
                announcement_data['course_id'] = course_data.get('id')
                announcement_data['course_name'] = course_data.get("name")
                announcement_data['course_code'] = course_data.get("course_code")

                new_unsent_announcements_data.append(announcement_data)
    
    return new_unsent_announcements_data


def get_announcement_channel(client, announcement_data):

    channel = client.get_channel(int(announcement_data.get('channel_id')))

    return channel


def mark_announcement_as_sent(id):
    sql_query_commit(query_update_announcement_sent(id))
    if(get_debug()):print(f'Announcement with {id} marked as sent.')


# Creates the embed for announcements in discord
def create_announcement_embed(announcement_data):

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

    # Course information
    course_name = announcement_data.get("name")
    course_code = announcement_data.get("course_code")
    course_id = announcement_data.get("course_id")
    
    # Embed layout
    embed = discord.Embed(title="New Announcement 📢", 
                          description=f"Course: {course_id}\n{course_name} | {course_code} \n", 
                          colour=0x98FB98)

    embed.set_author(name="CanvasDiscordBot", 
                    icon_url="https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180")

    embed.add_field(name=title, value=message_raw + "\n\n\n ", inline=False)
    embed.set_footer(text="Posted " + posted_at_formatted + f"\nby {author}")
    return embed

