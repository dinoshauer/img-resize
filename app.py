import argparse

from flask import Flask

import config
from resizer.routes import resizer
from utils.routes import utils

app = Flask(__name__)

config.load_config(app)
config.setup_logging(app)
app.register_blueprint(resizer)
app.register_blueprint(utils)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
