import discord

def error_message_embed(title, error_type, message, user_action):

    embed = discord.Embed(title=f'{title} ⚠️', 
                          description=f'{error_type}', 
                          colour=0x98FB98)

    embed.set_author(name='CanvasDiscordBot', 
                    icon_url='https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180')

    embed.add_field(name=f'{message}', value=f'{user_action}' + '\n\n\n ', inline=False)

    return embed