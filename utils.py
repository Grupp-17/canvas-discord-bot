# Misc utilities 

# Internal modules
import argparse
import json

# Third party modules
from bs4 import BeautifulSoup
from environs import load_dotenv

##############################
### Cmdline argument handler #
##############################

# Run only once
def init_cmdline_argument_parser():
    global debug

    # Init argparser
    parser = argparse.ArgumentParser(prog='Canvas Discord Bot')

    # Add argument for debugging and store argument as boolean in debug variable later
    parser.add_argument('-d', help='starts in debug mode', action='store_true', dest='debug')

    # Store result in debug variable
    args = parser.parse_args()

    # Return dictionary of argument keys and values
    debug = vars(args)['debug']


# In a function due to initiation order due to user cmd arguments vs modules
# The function is called after user input argument is parsed and debug variable is set
def get_debug():
    return debug

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

