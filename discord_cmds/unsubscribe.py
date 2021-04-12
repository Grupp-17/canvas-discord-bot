# Local modules
from database.interactions import \
    get_course_data, \
    sql_query_commit
from database.queries import \
    query_update_subscription, \
    query_update_channel_id
from discord_cmds.info_messages import \
    error_message_embed

# Third party modules
import discord

# TODO Want to be able to send reason for unsubscription to function as String
# TODO Needs to reset channel_id to 0 as well
def unsubscribe_command(course_id):

    # Query to get course data from a specific course
    course_data = get_course_data(f'id = {course_id}')

    if(course_data == None):

        embed = discord.Embed(colour=0x98FB98, description='🤷')
        embed.set_author(name='CanvasDiscordBot',
                        icon_url='https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180')
        embed.add_field(name=f'\n\nCourse {course_id} does not exist', value='Choose another course')

        return embed
    
    course_name = course_data.get('name')
    course_id = course_data.get('id')
    course_code = course_data.get('course_code')
    
    # Create embed if a course if already unsubscribed to
    if (course_data.get('subscribed_to') == '0'):
        embed = discord.Embed(colour=0x98FB98, description='🔕')
        embed.set_author(name='CanvasDiscordBot',
                        icon_url='https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180')
        embed.add_field(name=f'\n\nAlready unsubscribed to course {course_id}', value=f'{course_name} | {course_code}\n')
        
        return embed
    
    # Create embed for unsubscribing to a course
    else:

        if (commit_unsubscription(course_id) == True):
            embed = discord.Embed(colour=0x98FB98, description='🔕')
            embed.set_author(name='CanvasDiscordBot',
                            icon_url='https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180')
            embed.add_field(name=f'\n\nUnsubscribed to course {course_id}', value=f'{course_name} | {course_code}\n')
            embed.set_footer(text='Subscription removed ❌')
        
            return embed

        else:
            embed = error_message_embed("Database error", "Could not reach database!", "Bot is disabled", "Contact administrator!")
            return embed

def commit_unsubscription(course_id):
    
    if (sql_query_commit(query_update_subscription(course_id, '0')) and sql_query_commit(query_update_channel_id(course_id, '0'))):
        return True
    else:
        return False

