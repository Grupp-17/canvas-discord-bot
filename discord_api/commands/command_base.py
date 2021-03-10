# Refactor duplicated codeblocks from commands

from database.interactions import sql_query
from database.queries import sql_select_courses
from os import name
import random
from discord.ext import commands


class CommandBase(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="singla")
    async def singla(self, ctx):
        rand_int = random.randint(0, 1)
        if rand_int == 0:
            results = "Krona"
        else:
            results = "Klave"
        await ctx.send(results)

    @commands.command(name="courses")
    async def courses(self, ctx):
        results = sql_query(sql_select_courses)
        print(results)
        await ctx.send(results)

def setup(client):
    client.add_cog(CommandBase(client))