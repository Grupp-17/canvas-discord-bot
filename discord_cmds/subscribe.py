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
    subscribed = sql_query_fetchone_result(sql_select_table_attributes_condition("subscribed_to", "courses", f"id = {course_id}"))

    if subscribed == 1:
        return True
    else:
        return False

# TODO Rename to describe function
# Subscribe command
def subscribe_command(arg):

    # Query to get id, name, course_code from a specific course
    # TODO course_data might be better name?
    course_info = create_sql_query_list(sql_query_fetch(sql_select_table_attributes_condition("id, name, course_code", "courses", f"id == '{arg}'")))
    
    # Query to get id for all courses
    # TODO course_id_all
    id_query = create_sql_query_list(sql_query_fetch(sql_select_table_attributes("id", "courses")))

    # Check if course_info contains information
    if (course_info != []):

        # Split and store the information into variables
        course_id = course_info[0]
        course_name = course_info[1]
        course_code = course_info[2]

        # Embed layout
        embed = discord.Embed(colour=0x98FB98, description="🔔")
        embed.set_author(name="CanvasDiscordBot",
                        icon_url="https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180")
        
        # Check if course is subscribed to
        if is_subscribed(arg):

            embed.add_field(name=f"\n\nAlready subscribed to course {course_id}", value=f"{course_name} | {course_code}\n")
            embed.set_footer(text="No subscription added!")
        else:
            embed.add_field(name=f"\n\nSubscribed to course {arg}", value=f"{course_name} | {course_code}\n")
            embed.set_footer(text="Subscription added ✔️")

            # Update subscribed_to on the course that now is subscribed to
            sql_query_commit(sql_update_subscription(arg, "1"))

        return embed

    else:

        # If the course does not exist in the database,
        # send embed with information of the available courses

        all_courses_id = "\n".join(str(i) for i in id_query)
        embed = discord.Embed(colour=0x98FB98, description="🤷")
        embed.set_author(name="CanvasDiscordBot",
                        icon_url="https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180")
        embed.add_field(name=f"\n\nCourse '{arg}' does not exist", value=f"Avalible Courses:\n{all_courses_id}")
        embed.set_footer(text="No subscription added!")

        return embed
