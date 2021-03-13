# Internal modules
import random

# Local modules
from discord.ext.commands.core import command
from database.interactions import *
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
        
        course_names_query = sql_query_fetch(sql_select_table_attributes("name", "courses"))
        course_codes_query = sql_query_fetch(sql_select_table_attributes("course_code", "courses"))
        course_subscribed_query = sql_query_fetch(sql_select_table_attributes("subscribed_to", "courses"))
        id_query = sql_query_fetch(sql_select_table_attributes("id", "courses"))
        
        course_names = []
        course_codes = []
        course_subscribed = []
        id_list = []

        for names, codes, sub, id in zip(course_names_query, course_codes_query, course_subscribed_query, id_query):
            course_names.append(names[0])
            course_codes.append(codes[0])
            course_subscribed.append(sub[0])
            id_list.append(id[0])

        # Embed for displaying courses in discord
        embed = discord.Embed(title='Aktuella kurser', 
                              description="Här visas de aktuella kurserna", 
                              colour=0x98FB98)
        
        embed.set_author(name="CanvasDiscordBot", 
                         icon_url="https://play-lh.googleusercontent.com/2_M-EEPXb2xTMQSTZpSUefHR3TjgOCsawM3pjVG47jI-BrHoXGhKBpdEHeLElT95060B=s180")
        
        # Add fields in the embed by iterating through the lists
        for name, code, sub, id in zip(course_names, course_codes, course_subscribed, id_list):
            if sub == 1:
                sub = "✓"
            else:
                sub = " "
            embed.add_field(name=str(name) + " " + sub, value=code, inline=False)
        await ctx.send(embed=embed)
    
    def send_announcement():
        @commands.command(name="news")
        async def news(self, ctx):
        #     Get announcements query
        #     results = sql_query(sql_select_announcements)
        #     print(results)
            await ctx.send()

    @commands.command(name="subscribe")
    async def subscribe(self, ctx, *, arg):
    #   kolla igenom alla kurser, vilka kurser är redan subscribed?
        subscribe_query = sql_query_fetch(sql_select_table_attributes_condition(
                                            "id, name, subscribed_to",
                                            "courses",
                                            f"id == {arg} OR course_code == {arg} OR name == {arg}"))

        subscribed = [item for i in subscribe_query for item in i]

        if subscribed[2] == 1:
            message = f"Prenumererar redan på kurs {subscribed[0]}: {subscribed[1]}"
        else:
            message = f"Prenumererar på kurs {subscribed[0]}: {subscribed[1]}"

        await ctx.send(message)
    
    #   sätt värdet subscribed på kurs x i databasen till 1
    #   await ctx.send("Subscribe har lyckats till kurs x")

def setup(client):
    client.add_cog(CommandBase(client))