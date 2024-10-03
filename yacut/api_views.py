from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/<string:url_short>/', methods=['GET'])
def get_original_link(url_short):
    return jsonify(
        {'url': URLMap.validation_for_404(url_short)}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса',
                              HTTPStatus.BAD_REQUEST)
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!',
                              HTTPStatus.BAD_REQUEST)
    url = URLMap()
    custom_id = URLMap.validatator_custom_id(data)
    URLMap.short_id_validater(custom_id)
    url.from_dict(data)
    URLMap.save_db(url)
    return jsonify(url.to_dict()), HTTPStatus.CREATED
