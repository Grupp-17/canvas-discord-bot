# bot.py

# Internal modules
import os
import discord

from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Local modules
from database.init import init_database
from canvas.monitor import announcement_sent_mark, announcements_fetch, init_monitor

# Third party modules
import discord
from discord.ext import commands
from environs import load_dotenv

# Load private tokens
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

# Configure discord client
intents = discord.Intents.default()
client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='.')
initial_extensions = ['discord_api.commands.command_base']

if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)

# Main event handler for Discord client
@client.event
async def on_ready():

    print(f'{client.user} has connected to Discord!')

    # Init database (run once)
    init_success_database = init_database()

    # Continue only if init is successful
    if init_success_database:
        init_monitor()

    # Scheduler for sending announcements. Needs to be AysyncIO due to Discord client using the same
    announcement_scheduler = AsyncIOScheduler()

    # Add job to scheduler
    announcement_scheduler.add_job(announcement_handler, 'interval', seconds = 3)

    # Run scheduler
    announcement_scheduler.start()


@client.event
async def announcement_handler():
    
    # Set channel to .env token
    channel = client.get_channel(CHANNEL_ID)

    message_sent = False

    for message in announcements_fetch():
        message_sent = await channel.send(message)

        # If message was sent successfully mark it as sent
        if message_sent: 
            announcement_sent_mark(message)
        else:
            print(f'Message with id: {message} was not sent successfully!')


    # TODO Mark sent messages


client.run(DISCORD_TOKEN)
