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

class DevelopmentConfig(Config):
    DEBUG = True

def load_config(app, flags):
    if 'dev' in flags:
        app.config.from_object('config.DevelopmentConfig')
    else:
        app.config.from_object('config.Config')
