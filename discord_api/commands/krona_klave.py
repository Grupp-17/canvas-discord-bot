import random

def krona_klave(message, client):
    if message.author == client.user:
        return

    message_content = message.content.lower()

    if "singla" in message_content:
        rand_int = random.randint(0, 1)
        if rand_int == 0:
            results = "Krona"
        else:
            results = "Klave"
            
        return results
