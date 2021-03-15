# Misc utilities 

# Internal modules
import argparse

# Third party modules
from bs4 import BeautifulSoup

##############################
### Cmdline argument handler #
##############################

# Run only once
def init_cmdline_argument_parser():
    global debug

    # Init argparser
    parser = argparse.ArgumentParser(prog='Canvas Discord Bot')

    # Add argument for debugging and store argument as boolean in debug
    parser.add_argument('-d', help='starts in debug mode', action='store_true', dest='debug')

    # Store result in debug variable
    args = parser.parse_args()
    #arguments['debug'] = vars(args)['debug']

    # Return dictionary of argument keys and values
    debug = vars(args)['debug']


# TODO Comment
def get_debug():
    return debug

# TODO Comment
def html_to_raw(html_content):
    raw_content = BeautifulSoup(html_content, 'lxml')
    text = raw_content.get_text()

    return text