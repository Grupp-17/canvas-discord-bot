# Managing the announcement command

# Local modules
from utils import \
    get_config, \
    get_time_delta_days, \
    html_to_raw
from database.interactions import \
    get_all_courses_data, \
    get_all_announcements_data, \
    sql_query_commit
from database.queries import \
    query_update_announcement_sent 
from log_handler import \
    logger

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
        
        time_elapsed = get_time_delta_days(announcement.get('posted_at'))

        announcement_date_cut_off_time = int(get_config('announcement_date_cut_off_time'))

        # Check if not sent and if channel is set
        if(announcement.get('sent_discord') == '0') and (time_elapsed <= announcement_date_cut_off_time):

            unsent_announcements_data.append(announcement)

    return unsent_announcements_data


def join_courses_with_announcement_data(subscribed_courses_data, unsent_announcements_data):
    
    new_unsent_announcements_data = []

    for course_data in subscribed_courses_data:
        for announcement_data in unsent_announcements_data:
            context_code = announcement_data.get('context_code')

            # Checks that the join is done at the correct place
            if(context_code.strip('course_')) == (course_data.get('id')):
                
                # Add all needed data to dictionary from courses
                announcement_data['channel_id'] = course_data.get('channel_id')
                announcement_data['course_id'] = course_data.get('id')
                announcement_data['course_name'] = course_data.get('name')
                announcement_data['course_code'] = course_data.get('course_code')

                new_unsent_announcements_data.append(announcement_data)
    
    return new_unsent_announcements_data


def get_announcement_channel(client, announcement_data):

    channel = client.get_channel(int(announcement_data.get('channel_id')))

    return channel


def mark_announcement_as_sent(id):

    sql_query_commit(query_update_announcement_sent(id))
    
    logger.info(f'Announcement with {id} marked as sent.')


def shorten_announcement(announcement):
    
    short_announcement = announcement[0:1000] + "..."
    return short_announcement


# Creates the embed for announcements in discord
def create_announcement_embed(announcement_data):

    # Announcement information
    title = announcement_data.get('title')
    message = announcement_data.get('message')
    author = announcement_data.get('author')
    posted_at = announcement_data.get('posted_at').replace('T', ' at ')
    posted_at_formatted = posted_at.replace('Z', '')

    # Parse the text that is recieved in html
    # Shorten it so it fits in to the Discord embed
    message_raw = html_to_raw(message)
    message_content = shorten_announcement(message_raw)

    # Course information
    course_name = announcement_data.get('name')
    course_code = announcement_data.get('course_code')
    course_id = announcement_data.get('course_id')

    # Embed layout
    embed = discord.Embed(title='New Announcement 📢', 
                        description=f'Course: {course_id}\n{course_name} | {course_code} \n', 
                        colour=0xFEFDFD)

    embed.set_author(name='CanvasDiscordBot', 
                    icon_url='https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180')

    embed.add_field(name=title, value=message_content + '\n\n\n ', inline=False)
    embed.set_footer(text='Posted ' + posted_at_formatted + f'\nby {author}')

    return embed

