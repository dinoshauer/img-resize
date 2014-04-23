from flask import jsonify

def bad_argument(msg, arg):
    return jsonify(
        {
            'error': msg,
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
