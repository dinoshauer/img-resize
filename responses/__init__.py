from flask import jsonify

def bad_argument(arg):
    return jsonify(
        {
            'status': 'error',
            'error': 'missing argument: {}'.format(arg),
            'key': arg
        }
    ), 400

def success(data):
    return jsonify(
        {
            'status': 'ok',
            'data': data
        }
    ), 200

def created(data):
    return jsonify(
        {
            'status': 'created',
            'data': data
        }
    ), 201

def not_found():
    return jsonify(
        {
            'status': 'error',
            'error': 'not found'
        }
    ), 404
