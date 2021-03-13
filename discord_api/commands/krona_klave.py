import random

def krona_klave_command():
        rand_int = random.randint(0, 1)
        if rand_int == 0:
            results = "Krona"
        else:
            results = "Klave"
            
        return results
