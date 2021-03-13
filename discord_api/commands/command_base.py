# Internal modules
import random

# Local modules
from discord.ext.commands.core import command
from database.interactions import sql_query
from database.queries import *

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

        # Defining unwanted characters and replacing them with empty string
        def clean_string(string, list_of_char):
            for i in unwanted_chars:
                word = word.replace(i, "")
            return word

        unwanted_chars = ['[', ']', '"']
        # Import courses from db by sql-query
        course_names = clean_string(sql_query(sql_fetch_course_info("name", "courses"), unwanted_chars)).split(sep=",")
        course_codes = clean_string(sql_query(sql_fetch_course_info("course_codes", "courses"), unwanted_chars)).split(sep=",")
        course_id = clean_string(sql_query(sql_fetch_course_info("course_id", "courses"), unwanted_chars)).split(sep=",")
        id = clean_string(sql_query(sql_fetch_course_info("id", "courses"), unwanted_chars)).split(sep=",")

        # TODO Lägg till en bock om kursen är subscribed to
            
        # Embed for displaying courses in discord
        embed = discord.Embed(title='Aktuella kurser', 
                              description="Här visas de aktuella kurserna", 
                              colour=0x98FB98)
        
        embed.set_author(name="CanvasDiscordBot", 
                         icon_url="https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180")
        
        # Add fields in the embed by iterating through the lists
        for name, code, course_id, id in zip(course_names, course_codes, course_id, id):
            embed.add_field(name=str(name), value=code + " " + course_id + " " + id, inline=False)
        await ctx.send(embed=embed)
    
    def send_announcement():
        @commands.command(name="news")
        async def news(self, ctx):
        #     Get announcements query
        #     results = sql_query(sql_select_announcements)
        #     print(results)
            await ctx.send()

    ## @commands.command(name="subscribe",kurs)
    ## async def subscribe(self, ctx):
    #   kolla igenom alla kurser, vilka kurser är redan subscribed?
    #   sätt värdet subscribed på kurs x i databasen till 1
    #   await ctx.send("Subscribe har lyckats till kurs x")

def setup(client):
    client.add_cog(CommandBase(client))