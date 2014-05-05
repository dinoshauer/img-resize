import argparse

from flask import Flask

import config
from resizer.routes import resizer

parser = argparse.ArgumentParser(description='Runs the image resizer')
parser.add_argument('--debug', dest="mode", action="store_true", required=False, default=False, help='Run image resizer in debug mode.')
parser.add_argument('--production', dest="mode", action="store_false", required=False, default=False, help='Run image resizer in production mode.')
parser.add_argument('--port', type=int, required=False, default=5000, help='Port to run on')
parser.set_defaults(mode=False)
args = parser.parse_args()

app = Flask(__name__)

config.load_config(app, args.mode)
config.setup_logging(app)
app.register_blueprint(resizer)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=args.port)
