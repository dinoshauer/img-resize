import os
import json
from logging import Formatter
from logging.handlers import RotatingFileHandler
import logging

def _load_statsd_config(app):
    home = os.path.expanduser('~')
    statsd_config_file = '{}/.img-resizer'.format(home)
    if os.path.isfile(statsd_config_file):
        with open(statsd_config_file) as statsd_conf:
            config = json.loads(statsd_conf.read())
            app.config['STATSD']['host'] = config['statsd_host']
            app.config['STATSD']['port'] = config['statsd_port']

def load_config(app, args):
    if args.mode:
        app.config.from_object('config.config.DevelopmentConfig')
        app.config['STATSD']['host'] = 'localhost'
    else:
        app.config.from_object('config.config.Config')
        _load_statsd_config(app)

    if args.img_dir:
        app.config['IMG_DIR'] = args.img_dir
    if args.log_file:
        app.config['LOG_FILE'] = args.log_file

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
