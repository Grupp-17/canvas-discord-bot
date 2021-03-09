
import random

async def run_krona_klave(message):
    message_content = message.content.lower()
    
    if "singla" in message_content:
        rand_int = random.randint(0, 1)
        if rand_int == 0:
            results = "Krona"
        else:
            results = "Klave"
    await results