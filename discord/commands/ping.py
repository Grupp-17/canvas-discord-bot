# A ping pong command to check if bot is online
import discord
import os
from command_base import valid_permission, user

from environs import load_dotenv

command = "ping"

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print("{0.user} is online".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if valid_permission(user, command):
        if message.content.startswith('ping'):
            await message.channel.send('pong')

client.run(TOKEN)