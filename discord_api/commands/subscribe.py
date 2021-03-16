from database.interactions import *
from database.queries import *
import discord

# TODO Comments

def is_subscribed(course_id):
    subscribed = sql_query_fetchone_result(sql_select_table_attributes_condition("subscribed_to", "courses", f"id = {course_id}"))

    if subscribed == 1:
        return True
    else:
        return False

def subscribe_command(arg):

    course_info = create_sql_query_list(sql_query_fetch(sql_select_table_attributes_condition("id, name, course_code", "courses", f"id == '{arg}'")))
    id_query = create_sql_query_list(sql_query_fetch(sql_select_table_attributes("id", "courses")))

    if (course_info != []):
        course_id = course_info[0]
        course_name = course_info[1]
        course_code = course_info[2]
        embed = discord.Embed(colour=0x98FB98, description="🔔✔")
        embed.set_author(name="CanvasDiscordBot",
                        icon_url="https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180")
        if is_subscribed(arg):
            embed.add_field(name=f"\n\nAlready subscribed to course {course_id}", value=f"{course_name} | {course_code}\n")
            embed.set_footer(text="No subscription added!")
        else:
            embed.add_field(name=f"\n\nSubscribed to course {arg}", value=f"{course_name} | {course_code}\n")
            embed.set_footer(text="Subscription added ✔️")
            sql_query_commit(sql_update_subscription(arg, "1"))
            
            # TODO Remove checks or create suitable debugging message
            #check = sql_query_fetchone_result(sql_select_table_attributes_condition("subscribed_to", "courses", f"id = {arg}"))
            #print(check)
        return embed
    else:
        all_courses_id = "\n".join(str(i) for i in id_query)
        embed = discord.Embed(colour=0x98FB98, description="🤷")
        embed.set_author(name="CanvasDiscordBot",
                        icon_url="https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180")
        embed.add_field(name=f"\n\nCourse '{arg}' does not exist", value=f"Avalible Courses:\n{all_courses_id}")
        embed.set_footer(text="No subscription added!")
        return embed
