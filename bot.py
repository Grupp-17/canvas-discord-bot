# bot.py

# Internal modules
import os
import random

# Local modules
from database.init import init_database
from canvas.monitor import init_monitor
from discord_api.commands.krona_klave import run_krona_klave

# Third party modules
import discord
from environs import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
client = discord.Client(intents=intents)

client = discord.Client()

@client.event
async def on_ready():

    print(f'{client.user} has connected to Discord!')

    # Init database (run once)
    init_success_database = init_database()

    # Continue only if init is successful
    if init_success_database:
        init_monitor()

        # TODO 
        # Listen to commands
        # Start monitor

        # Get data from request



# This is just a test for pinging the bot
@client.event
async def on_message(message):
    result = run_krona_klave(message)
    await message.channel.send(result)

client.run(TOKEN)
