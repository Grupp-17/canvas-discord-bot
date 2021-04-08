# Registrering commands to Discord bot

# Internal modules
import os
from discord import channel

# Local modules
from discord.ext.commands.core import command
from database.interactions import *
from database.queries import *
from .courses import courses_command
from .subscribe import parse_arguments, match_channel, subscribe_command
from .unsubscribe import unsubscribe_command

# Third party modules
from discord.ext import commands

DEFAULT_CHANNEL_ID = int(os.getenv('DEFAULT_CHANNEL_ID'))

# Grouping the commands
class CommandBase(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Command for displaying the active courses
    @commands.command(name="courses")
    async def courses(self, ctx):
        await ctx.send(embed=courses_command(ctx))

    # Command for subscribing to courses
    # Set permission for the command
    @commands.command(name="subscribe")
    @commands.has_permissions(administrator=True)
    async def subscribe(self, ctx, *args):

        # Parse input arguments from user
        user_arguments  = parse_arguments(args)
        course_id = user_arguments[0]
        channel_id = user_arguments[1]
        
        if(channel_id != False):
            # Match and get correct channel data from Discord
            discord_channel_data = match_channel(ctx, channel_id)

            # Subscribe and send back confirmation message
            await ctx.send(embed=subscribe_command(course_id, channel_id, discord_channel_data))
        else:
            # TODO Proper error message
            await ctx.send('Too many arguments!')
   
    # Command to unsubscribe to a course
    # Set permission for the command
    @commands.command(name="unsubscribe")
    @commands.has_permissions(administrator=True)
    async def unsubscribe(self, ctx, arg):
        await ctx.send(embed=unsubscribe_command(arg))

# Add the group with commands to client
def setup(client):
    client.add_cog(CommandBase(client))