# Monotoring the information flow from canvas and the database

# Internal modules
import os

# Third party modules
import requests
from environs import load_dotenv

load_dotenv()
CANVAS_TOKEN = os.getenv('CANVAS_TOKEN')
CANVAS_DOMAIN = os.getenv('CANVAS_DOMAIN')

def fetch_courses():
    # TODO Get all available courses
    request = CANVAS_DOMAIN + f'/api/v1/courses?access_token=' + CANVAS_TOKEN
    
    # Send request
    response = send_request(request, 'courses')

    if response is not None:
        # Load JSON from response using built in JSON method and return it
        return response.json()
    else:
        return None


def send_request(request, type):

    # Send Get request
    try:
        response = requests.get(request)
        if response.status_code == 200:
            # TODO Check if data is correct
            print(f'Request {type} successful!')

            return response

        else:
            print('Error: ' + response.status_code)
            return None

    except requests.exceptions.RequestException as e:
        print(e) # Maybe SystemExit(e)? Should the program be allowed to continue?
        return None

