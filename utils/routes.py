from flask import Blueprint

utils = Blueprint(
    'utils',
    __name__,
    url_prefix='/v1/utils'
)

@utils.route('/ping', methods=['GET'])
def ping():
    return 'pong'
