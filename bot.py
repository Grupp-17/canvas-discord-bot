# bot.py

# Internal modules
import os

# Local modules
from database.init import init_database
from canvas.monitor import announcement_sent_mark, announcements_fetch, init_monitor
from utils import init_cmdline_argument_parser

# Third party modules
import discord
from discord.ext import commands
from discord_api.commands.announcement import announcement
from environs import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Load private tokens
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

# Configure discord client
intents = discord.Intents.default()
client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='.')
initial_extensions = ['discord_api.commands.command_base']

# Find out if debugging should be started (Only runs once)
init_cmdline_argument_parser()

# Important!!! Must be imported after cmdline parser has been initiated
# Else constants will not be set correctly
from utils import debug

if(debug):
    print('DEBUG ON')
else:
    print('DEBUG OFF')

# TODO is it necessary to load it here in main? Why not above?
if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)


###########################################
### Main event handler for Discord client #
###########################################

@client.event
async def on_ready():
    
    if(debug):print(f'{client.user} has connected to Discord!')

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

    print('Canvas Discord Bot has started!')


###########################################
# Discord bot announcements event handler #
###########################################

@client.event
async def announcement_handler():
    
    # Set channel to .env token
    channel = client.get_channel(CHANNEL_ID)

    message_sent = False

    for id in announcements_fetch():
        if (announcement(id) != 0):
            message_sent = await channel.send(embed=announcement(id))

        # If message was sent successfully mark it as sent
        if message_sent: 
            announcement_sent_mark(id)
        else:
            if(debug):print(f'Message with id: {id} was not sent successfully!')

client.run(DISCORD_TOKEN)
