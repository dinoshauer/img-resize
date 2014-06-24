from flask import jsonify

def bad_argument(arg):
    return jsonify(
        {
            'status': 'error',
            'error': 'missing argument: {}'.format(arg),
            'key': arg
        }
    ), 400

def not_found():
    return jsonify(
        {
            'status': 'error',
            'error': 'not found'
        }
    ), 404
