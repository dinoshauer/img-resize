from flask import Blueprint, current_app, jsonify, request, Response

from logic import ImageRetriever, Resizer
import responses


resizer = Blueprint(
    'resizer',
    __name__,
    url_prefix='/v1/resizer'
)

@resizer.route('/', methods=['GET'])
def get():
    try:
        r = Resizer(
            current_app.config['REDIS'],
            current_app.config['IMAGE_DIR'],
            current_app.config['REDIS_KEY_EXPIRE']
        )
        result = r.process(request.args)
        if result:
            return Response(
                result,
                mimetype='image/jpeg'
            )
        return responses.not_found()
    except KeyError, e:
        return responses.bad_argument(e.message)

@resizer.route('/direct', methods=['GET'])
def pass_through():
    try:
        r = Resizer(
            current_app.config['REDIS'],
            current_app.config['IMAGE_DIR'],
            current_app.config['REDIS_KEY_EXPIRE']
        )
        result = r.process_and_return(request.args)
        if result:
            return Response(
                result,
                mimetype='image/jpeg'
            )
        return responses.not_found()
    except KeyError, e:
        return responses.bad_argument(e.message)

@resizer.route('/img/<file_name>')
def get_file(file_name):
    r = ImageRetriever(current_app.config['REDIS'])
    result = r.get_file(file_name)
    if result:
        return Response(
            result,
            mimetype='image/jpeg'
        )
    return responses.not_found()
