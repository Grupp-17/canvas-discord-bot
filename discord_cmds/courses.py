# Courses command

# Local modules
from database.interactions import \
    get_all_courses_data

# Third party modules
import discord


def courses_command(ctx):

    # Get all courses data
    courses_data = get_all_courses_data()

    # Embed for displaying all availible courses in discord
    embed = discord.Embed(title='Avaliable courses',
                        colour=0xFEFDFD)
    
    embed.set_author(name='CanvasDiscordBot', 
                    icon_url='https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180')
    
    # Adding the fields in the embed by iterating through the list with courses data
    for i in courses_data:
        if i.get("subscribed_to") == "1":
            sub = '🔔'
        else:
            sub = ' '
        embed.add_field(name=i.get("name") + ' ' + sub, value=i.get("course_code") + ' | ' + i.get("id"), inline=False)
    return embed