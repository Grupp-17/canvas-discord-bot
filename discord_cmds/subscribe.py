# TODO Comment

# subscribe.py

# Local modules
from database.interactions import *
from database.queries import *

# Third party modules
import discord

# Checks if a course is subscribed to
def is_subscribed(course_id):

    # Query to get subscribed_to value from courses
    subscribed = sql_query_fetchone_result(query_select_table_attributes_condition("subscribed_to", "courses", f"id = {course_id}"))

    if subscribed == 1:
        return True
    else:
        return False

# TODO Rename to describe function
# Subscribe command
def subscribe_command(course_id_arg, channel_name_arg, discord_channel_data):

    # Data 
    # Query to get id, name, course_code from a specific course
    course_data = create_sql_query_list(sql_query_fetch(query_select_table_attributes_condition("id, name, course_code", "courses", f"id == '{course_id_arg}'")))

    # Query to get id for all courses
    course_id_all = create_sql_query_list(sql_query_fetch(query_select_table_attributes("id", "courses")))

    # Course ID not found - return error message to user
    if(course_data == []):

        all_courses_id = "\n".join(str(i) for i in course_id_all)
        embed = discord.Embed(colour=0x98FB98, description="🤷")
        embed.set_author(name="CanvasDiscordBot",
                        icon_url="https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180")
        embed.add_field(name=f"\n\nCourse '{course_id_arg}' does not exist", value=f"Available Courses:\n{all_courses_id}")
        embed.set_footer(text="No subscription added!")

        return embed

    # Channel not found - return error message to user
    elif(discord_channel_data == None):
        embed = discord.Embed(colour=0x98FB98, description="🤷")
        embed.set_author(name="CanvasDiscordBot",
                        icon_url="https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180")
        embed.add_field(name=f"\n\nChannel '{channel_name_arg}' does not exist!", value="Please try again!")

        return embed

    # Channel ID and Course ID found
    else:
        # Split and store the information into variables
        course_id = course_data[0]
        course_name = course_data[1]
        course_code = course_data[2]

        # Embed layout
        embed = discord.Embed(colour=0x98FB98, description="🔔")
        embed.set_author(name="CanvasDiscordBot",
                        icon_url="https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180")
        
        # Check if course is subscribed to
        if is_subscribed(course_id_arg):

            embed.add_field(name=f"\n\nAlready subscribed to course {course_id}", value=f"{course_name} | {course_code}\n")
            embed.set_footer(text="No subscription added!")
        
        # Commit changes and send ok message to user
        else:
            embed.add_field(name=f"\n\nSubscribed to course {course_id_arg}\nIn channel {discord_channel_data.name}", value=f"{course_name} | {course_code}\n")
            embed.set_footer(text="Subscription added ✔️")

            # Update subscribed_to on the course that now is subscribed to
            sql_query_commit(query_update_subscription(course_id_arg, "1"))
            
            # Update channel id for course
            sql_query_commit(query_update_channel_id(course_id_arg, discord_channel_data.id))

        return embed
