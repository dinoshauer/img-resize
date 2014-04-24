import sys

from flask import Flask

import config
from resizer.routes import resizer

app = Flask(__name__)

config.load_config(app, sys.argv)
config.setup_logging(app)
app.register_blueprint(resizer)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
