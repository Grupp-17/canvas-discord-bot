# Registrering commands to Discord bot

# Internal modules
import os

# Local modules
from discord.ext.commands.core import command
from database.interactions import *
from database.queries import *
from .courses import courses_command
from .subscribe import subscribe_command
from .unsubscribe import unsubscribe_command

# Third party modules
from discord.ext import commands
from discord.utils import get

DEFAULT_CHANNEL_ID = int(os.getenv('DEFAULT_CHANNEL_ID'))

# Grouping the commands
class CommandBase(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Command for displaying the active courses
    @commands.command(name="courses")
    async def courses(self, ctx):
        await ctx.send(embed=courses_command(ctx))

    # Command for subscribing to cources
    @commands.command(name="subscribe")
    async def subscribe(self, ctx, *args):

        # TODO Move to subscribe.py
        course_id_arg = args[0]

        # Check if channel is specified by user
        if(len(args) == 2):
            channel_name_arg = args[1]
        
        # If no course ID set fallback on default
        elif(len(args) == 1):
            channel_name_arg = DEFAULT_CHANNEL_ID

        # If too many arguments, return error message to user
        else:
            await ctx.send("Invalid amount of arguments!\nValid input: <prefix>courses <course id> <channel>")
            
        # Get channel data from Discord
        #discord_data = get(ctx.guild.text_channels, name = to_channel_name)

        for channel in ctx.guild.channels:
            if(channel.id) == channel_name_arg:
                discord_channel_data = get(ctx.guild.text_channels, name = channel.name)
                break
            elif(channel.name) == channel_name_arg:
                discord_channel_data = get(ctx.guild.text_channels, name = channel_name_arg)
                break
            else:
                discord_channel_data = None

        await ctx.send(embed=subscribe_command(course_id_arg, channel_name_arg, discord_channel_data))
   
    @commands.command(name="unsubscribe")
    async def unsubscribe(self, ctx, arg):
        await ctx.send(embed=unsubscribe_command(arg))

# Add the group with commands to client
def setup(client):
    client.add_cog(CommandBase(client))