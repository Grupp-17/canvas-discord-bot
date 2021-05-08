# Misc utilities 

# Internal modules
import argparse
import json
from datetime import \
    date
from datetime import \
    datetime

# Third party modules
from bs4 import BeautifulSoup

##############################
### Cmdline argument handler #
##############################

# Run only once
def get_debug():

    # Init argparser
    parser = argparse.ArgumentParser(prog='Canvas Discord Bot')

    # Add argument for debugging and store argument as boolean in debug variable later
    parser.add_argument('-d', help='starts in debug mode', action='store_true', dest='debug')

    # Store result in debug variable
    args = parser.parse_args()

    # Return dictionary of argument keys and values
    debug_arg = vars(args)['debug']

    return debug_arg
    
# TODO Comment
def html_to_raw(html_content):
    raw_content = BeautifulSoup(html_content, 'lxml')
    text = raw_content.get_text()

    return text

def get_config(option):
    # Load config
    with open('config.json') as config_file:
        config_data = json.load(config_file)

    return config_data[f'{option}']

def get_time_delta_days(posted_at):

    date_db = posted_at.split('T')[0]

    date_db_obj = datetime.strptime(date_db, '%Y-%m-%d')

    delta = date.today() - date_db_obj.date()

    return delta.days

# Function to set timestamp in database
def timestamp():
    return datetime.now().strftime('%Y:%m:%dT%I:%M:%S')