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
    IMAGE_DIR = '/home/ubuntu/img-resizer/resources'
    LOG_FILE = '/home/ubuntu/logs/img-resizer.log'
    STATSD = {
        'host': None,
        'port': 8125,
        'download_timer': 'img_resizer.download.timer',
        'resize_timer': 'img_resizer.resize.timer',
        'get_file_timer': 'img_resizer.get_file.timer',
        'cached_counter': 'img_resizer.cached_file.counter',
        'save_file_timer': 'img_resizer.save_file.timer',
        'process_request_timer': 'img_resizer.process_request_total.timer'
    }

class DevelopmentConfig(Config):
    DEBUG = True
