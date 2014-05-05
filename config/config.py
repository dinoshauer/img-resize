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
    STATSD = {
        'host': None,
        'port': 8125,
        'download_timer': 'img-resizer.download.timer',
        'resize_timer': 'img-resizer.resize.timer',
        'get_file_timer': 'img-resizer.get_file.timer',
        'cached_counter': 'img-resizer.cached_file.counter',
        'save_file_timer': 'img-resizer.save_file.timer'
    }

class DevelopmentConfig(Config):
    DEBUG = True
