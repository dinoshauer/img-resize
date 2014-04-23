import sys

from flask import Flask

from config import load_config
from resizer.routes import resizer

app = Flask(__name__)
load_config(app, sys.argv)
app.register_blueprint(resizer)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
