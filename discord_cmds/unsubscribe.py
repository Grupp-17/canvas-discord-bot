
from database.interactions import *
from database.queries import *

# Third party modules
import discord


def unsubscribe_command(course_id_arg):

    # Query to get course data from a specific course
    course_data = get_course_data(f"id == '{course_id_arg}'")
    
    course_name = course_data.get("name")
    course_id = course_data.get("id")
    course_code = course_data.get("course_code")

    # Query to get id for all courses
    course_id_all = create_sql_query_list(sql_query_fetch(query_select_table_attributes("id", "courses")))

    if(course_data == None):

        all_courses_id = "\n".join(str(i) for i in course_id_all)
        embed = discord.Embed(colour=0x98FB98, description="🤷")
        embed.set_author(name="CanvasDiscordBot",
                        icon_url="https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180")
        embed.add_field(name=f"\n\nCourse '{course_id_arg}' does not exist", value=f"Available Courses:\n{all_courses_id}")

        return embed

    elif (course_data.get("subscribe") == 0):

        embed = discord.Embed(colour=0x98FB98, description="🔕")
        embed.set_author(name="CanvasDiscordBot",
                        icon_url="https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180")
        embed.add_field(name=f"\n\nCourse {course_id} is not subscribed to", value=f"{course_name} | {course_code}\n")
        return embed
    

    elif (course_data.get("subscribe") == 1):
        embed = discord.Embed(colour=0x98FB98, description="🔕")
        embed.set_author(name="CanvasDiscordBot",
                        icon_url="https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180")
        embed.add_field(name=f"\n\nAlready unsubscribed to course {course_id}", value=f"{course_name} | {course_code}\n")

        sql_query_commit(query_update_subscription(course_data.get("id"), 0))
        
        return embed
    
    else:
        embed = discord.Embed(colour=0x98FB98, description="🔕")
        embed.set_author(name="CanvasDiscordBot",
                        icon_url="https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180")
        embed.add_field(name=f"\n\nUnsubscribed to course {course_id}", value=f"{course_name} | {course_code}\n")
        embed.set_footer(text="Subscription removed ❌")

        sql_query_commit(query_update_subscription(course_data.get("id"), 0))
        
        return embed