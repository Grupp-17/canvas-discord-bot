# Internal modules
import random

# Local modules
from discord.ext.commands.core import command
from database.interactions import sql_query
from database.queries import sql_select_courses

# Third party modules
import discord
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

    ## Command for displaying the active courses

    @commands.command(name="courses")
    async def courses(self, ctx):
        
        # Import courses from db by sql-query
        q = sql_query(sql_select_courses)

        # Defining unwanted characters and replacing them with empty string
        unwanted_chars = ['[', ']', '"']
        for i in unwanted_chars:
            q = q.replace(i, "")

        # Split strings to separate each course
        results = q.split(sep=",")

        # Separate course names and course codes into different lists
        for i in results:
            course_names = results[::2]
            course_codes = results[1::2]
            
        # Embed for displaying courses in discord
        embed = discord.Embed(title='Aktuella kurser', 
                              description="Här visas de aktuella kurserna", 
                              colour=0x98FB98)
        
        embed.set_author(name="CanvasDiscordBot", 
                         icon_url="https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180")
        
        # Add fields in the embed by iterating through the lists
        for i, j in zip(course_names, course_codes):
                embed.add_field(name=str(i), value=str(j), inline=False)
        await ctx.send(embed=embed)
    
    @commands.command(name="news")
    async def news(self, ctx):
    #     # Get announcements query
    #     results = sql_query(sql_select_announcements)
    #     print(results)
        await ctx.send()

def setup(client):
    client.add_cog(CommandBase(client))