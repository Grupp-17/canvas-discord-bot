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
from database.queries import sql_select_table_attributes_condition
from database.interactions import sql_query_fetchone_result
from canvas.monitor import announcement_sent_mark, announcements_fetch, init_monitor
from utils import init_cmdline_argument_parser, get_debug
from discord_cmds.announcement import announcement

# Third party modules
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from environs import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils import get_config

# Load private tokens
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DEFAULT_CHANNEL_ID = int(os.getenv('DEFAULT_CHANNEL_ID'))

# Configure discord client
intents = discord.Intents.default()
client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='.')
initial_extensions = ['discord_cmds.command_base']

# Find out if debugging should be started (only runs once)
init_cmdline_argument_parser()

if(get_debug()):
    print('DEBUG ON')
else:
    print('DEBUG OFF')


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
        # Start update loop for db to fetch data from Canvas domain
        init_monitor()

    # Scheduler for sending announcements. Needs to be AysyncIO due to Discord client using the same
    # This scheduler will check regularly if a course in the database is subscribed to. If that is
    # the case: send unsent announcements.
    announcement_scheduler = AsyncIOScheduler()

    # Add job to scheduler
    announcement_scheduler.add_job(announcement_handler, 'interval', seconds=get_config('announcement_scheduler_interval'))

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

    message_sent = False

    for id in announcements_fetch():
        if (announcement(id) != None):

            # TODO Find a nicer way to do this
            context_code = sql_query_fetchone_result(sql_select_table_attributes_condition('context_code', 'announcements', f'id = {id}'))
            course_id = context_code.strip("course_")
            channel_id = sql_query_fetchone_result(sql_select_table_attributes_condition('channel_id', 'courses', f'id = {course_id}'))
            channel = client.get_channel(channel_id)
            
            if channel != None:
                message_sent = await channel.send(embed=announcement(id))
            
            # If text channel is deleted 
            else:
                # TODO Unsubscribe
                channel = client.get_channel(DEFAULT_CHANNEL_ID)
                await channel.send(f'Channel not found!\nID: {channel.id}\nName: {channel.name}\nSubscription removed')

        # TODO Move to announcement. Should be handled in annoucement not in bot. If message was sent successfully mark it as sent
        if message_sent: 
            announcement_sent_mark(id)
            message_sent = False
        else:
            if(get_debug()):print(f'Message with id: {id} was not sent')

client.run(DISCORD_TOKEN)
