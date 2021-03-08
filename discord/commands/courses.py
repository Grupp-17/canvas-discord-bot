# Courses command to display all courses from Canvas

import discord
from discord.ext import commands
import os

from environs import load_dotenv

courses_list = ["Course1", "Course2"]

# TODO put in commandbase?
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    print("{0.user} is online".format(client))


@client.command()
async def courses(ctx):
	await ctx.channel.send(courses_list)

client.run(TOKEN)