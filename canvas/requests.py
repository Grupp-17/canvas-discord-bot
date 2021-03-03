# Monotoring the information flow from canvas and the database

# Internal modules
import os

# Third party modules
import requests
from environs import load_dotenv

load_dotenv()
CANVAS_TOKEN = os.getenv('CANVAS_TOKEN')
CANVAS_DOMAIN = os.getenv('CANVAS_DOMAIN')

def send_request(type):

    getRequest = CANVAS_DOMAIN + f'/api/v1/courses/1?access_token=' + CANVAS_TOKEN
    #getRequest = 'http://canvas.winkit.se:8080/api/v1/courses/1?access_token=4JoDTcLc8DgxlGm3K5o7Hub8ffshDCSugscQrARnqHLAcapbe8a8FeykBa7SE6cQ'
    
    # Send Get request
    try:
        response = requests.get(getRequest)
    except requests.exceptions.RequestException as e:
        print(e) # Maybe SystemExit(e)? Should the program be allowed to continue?

    # Load JSON from response using built in JSON method
    data = response.json()

    print(f'Request {type} successful!')

    return data
