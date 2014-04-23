import sys

from flask import Flask

from config import load_config

app = Flask(__name__)
load_config(app, sys.argv)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
