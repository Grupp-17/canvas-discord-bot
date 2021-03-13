# bot.py

# Internal modules
import os

# Local modules
from database.init import init_database
from canvas.monitor import init_monitor

# Third party modules
import discord
from discord.ext import commands
from environs import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
client = discord.Client(intents=intents)

client = commands.Bot(command_prefix='.')

initial_extensions = ['discord_api.commands.command_base']

if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)

@client.event
async def on_ready():

    print(f'{client.user} has connected to Discord!')

    # Init database (run once)
    init_success_database = init_database()

    # Continue only if init is successful
    if init_success_database:
        init_monitor()


client.run(TOKEN)
