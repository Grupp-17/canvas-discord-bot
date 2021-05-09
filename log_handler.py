# Local modules
import logging
from logging.handlers import RotatingFileHandler

# Internal modules
from utils import \
    get_config, \
    get_debug

# Create logger
logger = logging.getLogger()

# How the log data is formatted
log_format = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] [%(module)s] [%(lineno)d] %(message)s')

RotatingFileHandler('logs/debug.log', maxBytes=2000, backupCount=10)

if(get_config('debug_log') or get_debug()):
    logger.setLevel(logging.DEBUG)
    file_handler = RotatingFileHandler('logs/debug.log', maxBytes=2000000, backupCount=10)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    print('DEBUG MODE | Output: logs/debug.log')
else:    
    logger.setLevel(logging.WARNING)
    file_handler = RotatingFileHandler('logs/error.log', maxBytes=2000000, backupCount=10)
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)
