
from database.interactions import *
from database.queries import *

# Third party modules
import discord

# TODO Want to be able to send reason for unsubscription to function as String
# TODO Needs to reset channel_id to 0 as well
def unsubscribe_command(course_id):

    # Query to get course data from a specific course
    course_data = get_course_data(f"id = '{course_id}'")

    if(course_data == None):

        embed = discord.Embed(colour=0x98FB98, description="🤷")
        embed.set_author(name="CanvasDiscordBot",
                        icon_url="https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180")
        embed.add_field(name=f"\n\nCourse '{course_id}' does not exist", value="Choose another course")

        return embed
    
    course_name = course_data.get("name")
    course_id = course_data.get("id")
    course_code = course_data.get("course_code")

    # Query to get id for all courses
    course_id_all = create_sql_query_list(sql_query_fetch(query_select_table_attributes("id", "courses")))
    

    if (course_data.get("subscribed_to") == "0"):
        embed = discord.Embed(colour=0x98FB98, description="🔕")
        embed.set_author(name="CanvasDiscordBot",
                        icon_url="https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180")
        embed.add_field(name=f"\n\nAlready unsubscribed to course {course_id}", value=f"{course_name} | {course_code}\n")
        
        return embed
    
    else:
        embed = discord.Embed(colour=0x98FB98, description="🔕")
        embed.set_author(name="CanvasDiscordBot",
                        icon_url="https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180")
        embed.add_field(name=f"\n\nUnsubscribed to course {course_id}", value=f"{course_name} | {course_code}\n")
        embed.set_footer(text="Subscription removed ❌")

        sql_query_commit(query_update_subscription(course_data.get("id"), 0))
        sql_query_commit(query_update_channel_id(course_data.get("channel_id"), 0))
        
        return embed