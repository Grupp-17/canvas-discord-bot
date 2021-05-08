# Local modules
import logging

# Internal modules
from utils import \
    get_config, \
    get_debug

# Create logger
logger = logging.getLogger()

# How the log data is formatted
log_format = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s')

if(get_config('debug_log') or get_debug()):
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('debug.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    print('DEBUG MODE -> debug.log')
else:    
    logger.setLevel(logging.WARNING)
    file_handler = logging.FileHandler('error.log')
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)
