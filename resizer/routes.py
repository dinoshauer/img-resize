from flask import Blueprint, current_app, jsonify, request

from logic import Resizer
import responses


resizer = Blueprint(
    'resizer',
    __name__,
    url_prefix='/v1/resizer'
)

@resizer.route('/', methods=['GET'])
def get():
    try:
        r = Resizer(current_app.config['REDIS'], current_app.config['IMAGE_DIR'])
        result = r.process(request.args)
        return jsonify(result[0]), result[1]
    except KeyError, e:
        return responses.bad_argument(e.message, e.message)
