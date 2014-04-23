from flask import Blueprint, current_app, jsonify, request

import responses


resizer = Blueprint(
    'resizer',
    __name__,
    url_prefix='/v1/resizer'
)

@resizer.route('/', methods=['GET'])
def get():
    try:
        request.args
    except KeyError, e:
        return responses.bad_argument(e.message, e.message)
