import os
from logging import Formatter
from logging.handlers import RotatingFileHandler
import logging

def load_config(app, debug):
    if debug:
        app.config.from_object('config.config.DevelopmentConfig')
    else:
        app.config.from_object('config.config.Config')
        app.config['STATSD']['host'] = os.environ.get('IMG_RESIZER_STATSD_HOST')
        app.config['STATSD']['port'] = os.environ.get('IMG_RESIZER_STATSD_PORT')

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
