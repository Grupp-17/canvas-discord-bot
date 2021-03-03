# bot.py
import os
import random

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

# This is just a test for pinging the bot
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    message_content = message.content.lower()
    if "singla" in message_content:
        rand_int = random.randint(0, 1)
        if rand_int == 0:
            results = "Krona"
        else:
            results = "Klave"
        await message.channel.send(results)

client.run(TOKEN)
