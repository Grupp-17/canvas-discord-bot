import discord

def error_message_embed(title, error_description, message, user_action):

    embed = discord.Embed(title=f'{title} ⚠️', 
                          description=f'{error_description}', 
                          colour=0xFEFDFD)

    embed.set_author(name='CanvasDiscordBot', 
                    icon_url='https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180')

    embed.add_field(name=f'{message}', value=f'{user_action}' + '\n\n\n ', inline=False)

    return embed

def not_found_message_embed(title, message, user_action):
    
    embed = discord.Embed(colour=0xFEFDFD, description="🤷")
    embed.set_author(name="CanvasDiscordBot",
                    icon_url="https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180")
    
    embed.add_field(name=f"{title}", value=f"{user_action}")
    embed.set_footer(text=f"{message}")

    return embed
