# Copyright 2021 Andreas Kalin Winkler, Tove Andersson, Josef Gunnarsson

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# bot.py

# Internal modules
import os

# Local modules
from database.init import init_database
from canvas.monitor import announcement_sent_mark, announcements_fetch, init_monitor
from utils import init_cmdline_argument_parser, get_debug
from discord_cmds.announcement import announcement

# Third party modules
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
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
initial_extensions = ['discord_cmds.command_base']

# Find out if debugging should be started (Only runs once)
init_cmdline_argument_parser()

# Important!!! Must be imported after cmdline parser has been initiated
# Else constants will not be set correctly
from utils import debug

if(get_debug()):
    print('DEBUG ON')
else:
    print('DEBUG OFF')


if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)


###########################################
### Main event handler for Discord client #
###########################################

@client.event
async def on_ready():
    
    if(get_debug()):print(f'{client.user} has connected to Discord!')

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

# TODO Proper error handling
# Managing command error, ignoring invalid commands
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send('That command does not exist!')


###########################################
# Discord bot announcements event handler #
###########################################

@client.event
async def announcement_handler():
    
    # Set channel to .env token
    channel = client.get_channel(CHANNEL_ID)

    message_sent = False

    for id in announcements_fetch():
        if (announcement(id) != None):
            message_sent = await channel.send(embed=announcement(id))

        # If message was sent successfully mark it as sent
        if message_sent: 
            announcement_sent_mark(id)
            message_sent = False
        else:
            if(get_debug()):print(f'Message with id: {id} was not sent')

client.run(DISCORD_TOKEN)
