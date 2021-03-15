# TODO Comment needed

# Local modules
from utils import html_to_raw

# Third party modules
from database.interactions import *
from database.queries import *
from discord_api.commands.subscribe import is_subscribed
import discord

# TODO Comments

def announcement(announcement_id):
    # Check which context_code id has
    context_code = sql_query_fetchone_result(sql_select_table_attributes_condition("context_code", "announcements", f"id = {announcement_id}"))
    course_id = context_code.strip("course_")
    
    if is_subscribed(course_id):
        return create_announcements_embed(announcement_id, course_id)
    else:
        return None

def create_announcements_embed(announcement_id, course_id):

    announcement = create_sql_query_list(sql_query_fetch(sql_select_table_attributes_condition("*", "announcements", f"id = '{announcement_id}'")))
    course = create_sql_query_list(sql_query_fetch(sql_select_table_attributes_condition("*", "courses", f"id = '{course_id}'")))

    id = announcement[0]
    title = announcement[1]
    message = announcement[2]
    author = announcement[3]
    context_code = announcement[4]
    posted_at = announcement[5].replace("T", " at ")
    posted_at_formatted = posted_at.replace("Z", "")

    title_raw = html_to_raw(title)
    message_raw = html_to_raw(message)
    course_name = course[1]
    course_code = course[2]
    c_id = course[0]
    
    embed = discord.Embed(title="New Announcement!", 
                          description=f"{course_name} | {course_code} \n", 
                          colour=0x98FB98)

    embed.set_author(name="CanvasDiscordBot", 
                    icon_url="https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180")

    embed.add_field(name=title, value=message_raw + f"\n\n\nCourse {c_id}", inline=False)
    embed.set_footer(text="Posted " + posted_at_formatted)
    return embed