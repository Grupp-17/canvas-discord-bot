# HTTP requests for Canvas API

# Internal modules
import os

# Local modules
from log_handler import \
    logger

# Third party modules
import requests
from requests.structures import \
    CaseInsensitiveDict
from environs import \
    load_dotenv

# Get private TOKENS from .env
load_dotenv()
CANVAS_TOKEN = os.getenv('CANVAS_TOKEN')
CANVAS_DOMAIN = os.getenv('CANVAS_DOMAIN')

# Set request headers for authentication
headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Authorization"] = f"Bearer {CANVAS_TOKEN}"

#count = 0

def send_request(request, type):
    #global count
    #print(count)

    # Send Get request
    try:
        response = requests.get(request, headers = headers)
        if response.status_code == 200:
            # TODO Check if data is correct
            logger.info(f'Request {type} successful!')
            logger.debug(f'Respone from {CANVAS_DOMAIN}: {response}')
            #count += 1

            return response

        else:
            # If response from server is not ok, continue but do not terminate program.
            logger.error(f'Error request {type}: {response.status_code}')
            return None

    except requests.exceptions.RequestException as e:
        logger.error(f'{e}')
        


def fetch_courses():

    # Construct request URL
    request = f'{CANVAS_DOMAIN}/api/v1/courses'
    
    # Send request
    response = send_request(request, 'courses')
    logger.debug(f'Courses fetched: {response}')

    if response is not None:
        # Load JSON from response using built in JSON method and return it
        return response.json()
    else:
        return None


def fetch_announcements(context_code_id):

    # Construct request URL
    request = f'{CANVAS_DOMAIN}/api/v1/announcements?context_codes[]=course_{context_code_id}'

    # Send request
    response = send_request(request, 'announcements')
    logger.debug(f'Announcement fetched [{context_code_id}]: {response}')

    if response is not None:
        # Load JSON from response using built in JSON method and return it
        return response.json()
    else:
        return None
