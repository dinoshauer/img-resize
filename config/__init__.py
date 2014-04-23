class Config:
    DEBUG = False
    TESTING = False
    REDIS = 'redis://localhost:6379/1'

class DevelopmentConfig(Config):
    DEBUG = True

def load_config(app, flags):
    if ['dev', 'debug'] in flags:
        app.config.from_object('config.DevelopmentConfig')
    else:
        app.config.from_object('config.Config')
