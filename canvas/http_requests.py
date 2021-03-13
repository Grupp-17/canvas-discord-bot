# Monotoring the information flow from canvas and the database

# Internal modules
import os

# Third party modules
import requests
from requests.structures import CaseInsensitiveDict
from environs import load_dotenv

# Get private TOKENS from .env
load_dotenv()
CANVAS_TOKEN = os.getenv('CANVAS_TOKEN')
CANVAS_DOMAIN = os.getenv('CANVAS_DOMAIN')

# Set request headers
headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Authorization"] = f"Bearer {CANVAS_TOKEN}"


def send_request(request, type):

    # Send Get request
    try:
        response = requests.get(request, headers = headers)
        if response.status_code == 200:
            # TODO Check if data is correct
            print(f'Request {type} successful!')

            return response

        else:
            print(f'Error request {type}: {response.status_code}')
            return None

    except requests.exceptions.RequestException as e:
        print(e) # Maybe SystemExit(e)? Should the program be allowed to continue?
        return None


def fetch_courses():

    # Construct request URL
    request = f'{CANVAS_DOMAIN}/api/v1/courses'
    
    # Send request
    response = send_request(request, 'courses')

    if response is not None:
        # Load JSON from response using built in JSON method and return it
        return response.json()
    else:
        return None


def fetch_announcements(context_code_id):

    # Construct request URL
    request = f'{CANVAS_DOMAIN}/api/v1/announcements?context_codes[]=course_{context_code_id}'
    print(request)
    # Send request
    response = send_request(request, 'announcements')

    if response is not None:
        # Load JSON from response using built in JSON method and return it
        return response.json()
    else:
        return None
