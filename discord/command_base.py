# Registrering commands to Discord bot

# Local modules
from discord.ext.commands.core import command
from database.interactions import *
from database.queries import *
from .courses import courses_command
from .subscribe import subscribe_command

# Third party modules
from discord.ext import commands

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
    async def subscribe(self, ctx, *, arg):
        await ctx.send(embed=subscribe_command(arg))
   
# Add the group with commands to client
def setup(client):
    client.add_cog(CommandBase(client))