# Internal modules
import random

# Local modules
from discord.ext.commands.core import command
from database.interactions import *
from database.queries import *
from discord_api.commands.courses import courses_command
from discord_api.commands.krona_klave import krona_klave_command
from discord_api.commands.subscribe import subscribe_command
from discord_api.commands.news import news

# Third party modules
import discord
from discord.ext import commands


class CommandBase(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="singla")
    async def singla(self, ctx):
        await ctx.send(krona_klave_command())

    # Command for displaying the active courses

    @commands.command(name="courses")
    async def courses(self, ctx):
        await ctx.send(embed=courses_command(ctx))
    
    
    @commands.command(name="news")
    async def news(self, ctx):
        await ctx.send(news())

    @commands.command(name="subscribe")
    async def subscribe(self, ctx, *, arg):
        await ctx.send(subscribe_command(arg))
   

def setup(client):
    client.add_cog(CommandBase(client))