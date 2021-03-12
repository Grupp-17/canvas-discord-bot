# Refactor duplicated codeblocks from commands

import discord
from discord.ext.commands.core import command
from database.interactions import sql_query
from database.queries import *
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

    ## Command for displaying the active courses

    @commands.command(name="courses")
    @commands.guild_only()
    async def courses(self, ctx):
        
        # Import courses from db by sql-query
        course_name = sql_query(sql_select_course_name)
        course_id = sql_query(sql_select_course_id)


        # Defining unwanted characters and replacing them with empty string
        unwanted_chars = ['[', ']', '"']
        for i in unwanted_chars:
            course_name = course_name.replace(i, "")
            course_id = course_id.replace(i, "")
        # Split strings to separate each course
        names = course_name.split(sep=",")
        id= course_id.split(sep=",")

        # Embed for displaying courses in discord
        embed = discord.Embed(title='Aktuella kurser', 
                              description="Här visas de aktuella kurserna", 
                              colour=0x98FB98)
        embed.set_author(name="CanvasDiscordBot", 
                         icon_url="https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180")
        
        # Add fields in the embed
        for i in names:
            for j in id:
                embed.add_field(name=i, value=j, inline=False)
                await ctx.send(embed=embed)
    
    # @commands.command(name="news")
    # async def news(self, ctx):
    #     # Get announcements query
    #     results = sql_query(sql_select_announcements)
    #     print(results)
    #     await ctx.send(results)

def setup(client):
    client.add_cog(CommandBase(client))