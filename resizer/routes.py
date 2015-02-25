from flask import Blueprint, current_app, jsonify, request, Response

from logic import ImageRetriever, Resizer
import responses


resizer = Blueprint(
    'resizer',
    __name__,
    url_prefix='/img-resizer/v1/resizer'
)

@resizer.route('/', methods=['GET'])
def pass_through():
    try:
        r = Resizer(
            current_app.config['REDIS'],
            current_app.config['IMAGE_DIR'],
            statsd_config=current_app.config['STATSD'],
            key_expire=current_app.config['REDIS_KEY_EXPIRE']
        )
        result = r.process_and_return(request.args)
        if result:
            return Response(result, mimetype='image/jpeg')
        return responses.not_found()
    except KeyError, e:
        return responses.bad_argument(e.message)
