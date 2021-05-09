import discord

def error_message_embed(title, error_description, message, user_action):

    embed = discord.Embed(title=f'{title} ⚠️', 
                          description=f'{error_description}', 
                          colour=0xFEFDFD)

    embed.set_author(name='CanvasBot', 
                    icon_url='https://github.com/Grupp-17/canvas-discord-bot/blob/main/images/canvasboticon.png?raw=true')

    embed.add_field(name=f'{message}', value=f'{user_action}' + '\n\n\n ', inline=False)

    return embed

def not_found_message_embed(title, message, user_action):
    
    embed = discord.Embed(colour=0xFEFDFD, description="🤷")
    embed.set_author(name="CanvasBot",
                    icon_url="https://github.com/Grupp-17/canvas-discord-bot/blob/main/images/canvasboticon.png?raw=true")
    
    embed.add_field(name=f"{title}", value=f"{user_action}")
    embed.set_footer(text=f"{message}")

    return embed
