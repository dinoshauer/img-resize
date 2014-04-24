from logging import Formatter
from logging.handlers import RotatingFileHandler
import logging

class Config:
    DEBUG = False
    TESTING = False
    REDIS = {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'password': None
    }
    REDIS_KEY_EXPIRE = 604800  # a week in seconds
    IMAGE_DIR = './resources'
    LOG_FILE = 'app.log'

class DevelopmentConfig(Config):
    DEBUG = True


def load_config(app, flags):
    if 'dev' in flags:
        app.config.from_object('config.DevelopmentConfig')
    else:
        app.config.from_object('config.Config')

def rotating_handler(filename):
    if filename.startswith('~'):
        filename = filename.replace('~', os.path.expanduser('~'))
    handler = RotatingFileHandler(filename, maxBytes=5242880, backupCount=2)
    formatter = Formatter('%(asctime)s [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    return handler

def setup_logging(app):
    if not app.debug:
        filename = app.config['LOG_FILE']
        handler = rotating_handler(filename)
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)
