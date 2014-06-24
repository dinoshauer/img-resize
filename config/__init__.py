import os
import json
from logging import Formatter
from logging.handlers import RotatingFileHandler
import logging

def _load_statsd_config(app, path=None):
    if not path:
        home = os.path.expanduser('~')
        path = '{}/.img-resizer'.format(home)
    if os.path.isfile(path):
        with open(path) as statsd_conf:
            config = json.loads(statsd_conf.read())
            app.config['STATSD']['host'] = config['statsd_host']
            app.config['STATSD']['port'] = config['statsd_port']

def load_config(app):
    testing = os.environ.get('IMG_RESIZER_TESTING')
    deving = os.environ.get('IMG_RESIZER_DEV')
    BASE_DIR = os.getcwd()
    if testing:
        app.config.from_object('config.config.TestingConfig')
        app.config['STATSD']['host'] = 'localhost'
        app.config['IMG_DIR'] = '{}/resources'.format(BASE_DIR)
        app.config['LOG_FILE'] = '{}/img-resizer.log'.format(BASE_DIR)
    elif deving:  # pragma: no cover
        app.config.from_object('config.config.DevelopmentConfig')
        app.config['STATSD']['host'] = 'localhost'
        app.config['IMG_DIR'] = '{}/resources'.format(BASE_DIR)
        app.config['LOG_FILE'] = '{}/img-resizer.log'.format(BASE_DIR)
    else:  # pragma: no cover
        app.config.from_object('config.config.Config')
        _load_statsd_config(app)

def rotating_handler(filename):
    if filename.startswith('~'):
        filename = filename.replace('~', os.path.expanduser('~'))
    handler = RotatingFileHandler(filename, maxBytes=5242880, backupCount=2)
    formatter = Formatter('%(asctime)s [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    return handler

def stdout_handler():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s'))
    return handler

def setup_logging(app):
    if not app.debug:
        filename = app.config['LOG_FILE']
        try:
            handler = rotating_handler(filename)
        except IOError, e:
            handler = stdout_handler()
            print 'Falling back to stdout handler due to IOError'
            print e
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)
