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
