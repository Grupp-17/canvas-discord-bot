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
from database.init import \
    init_database
from canvas.monitor import \
    init_monitor
from discord_cmds.announcement import \
    get_subscribed_courses_data, get_unsent_announcements_data, \
    join_courses_with_announcement_data, \
    get_announcement_channel, \
    create_announcement_embed, \
    mark_announcement_as_sent
from discord_cmds.unsubscribe import \
    unsubscribe_command
from utils import \
    get_config
from log_handler import \
    logger

# Third party modules
import discord
from discord.ext import \
    commands
from discord.ext.commands import \
    CommandNotFound
from environs import \
    load_dotenv
from apscheduler.schedulers.asyncio import \
    AsyncIOScheduler


# Load enviromental variables
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_PREFIX = os.getenv('DISCORD_PREFIX')
DEFAULT_CHANNEL_ID = int(os.getenv('DEFAULT_CHANNEL_ID'))

# Configure discord client
intents = discord.Intents.default()
client = discord.Client(intents=intents)
client = commands.Bot(command_prefix=DISCORD_PREFIX.strip(''))
initial_extensions = ['discord_cmds.command_base']

for extension in initial_extensions:
    client.load_extension(extension)


###########################################
### Main event handler for Discord client #
###########################################

@client.event
async def on_ready():
    
    logger.info(
        f'{client.user} has connected to Discord!'
    )

    # Init database (run once)
    init_database()

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

    # Courses data
    subscribed_courses_data = get_subscribed_courses_data()

    # Announcement data
    unsent_announcements_data = get_unsent_announcements_data()

    # Check if there are unsent announcements
    if(unsent_announcements_data):

        # Join relevant data from subscribed courses data to unsent announcement data
        unsent_announcements_data = join_courses_with_announcement_data(subscribed_courses_data, unsent_announcements_data)

        # Set success state variable
        message_sent = False

        # Loop through unsent announcements and send them
        for announcement_data in unsent_announcements_data:

            # Send to correct channel
            channel = get_announcement_channel(client, announcement_data)

            if(channel):
                message_sent = await channel.send(embed=create_announcement_embed(announcement_data))
            
            # If no channel is found
            else:
                # Send error message to default channel and unsubscribe
                channel = client.get_channel(DEFAULT_CHANNEL_ID)

                # TODO This should be sent as error message
                await channel.send(f"Channel with ID: {announcement_data.get('channel_id')} not found! Unsubscribing to channel!")

                # Unsubscribe to course
                await channel.send(embed=unsubscribe_command(announcement_data.get('course_id')))
            
            if message_sent: 
                mark_announcement_as_sent(announcement_data.get('id'))

                # Reset success state variable for next iteration
                message_sent = False
            else:
                logger.warning(
                    f"Message with id: {announcement_data.get('id')} was not sent"
                )
                

client.run(DISCORD_TOKEN)
