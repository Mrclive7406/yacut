import re
from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from settings import CUSTOM_REGEXP_ID_MODEL, CUSTOM_REGEXP, MIDDL_LENGTH

INVALID_NAME = 'Указано недопустимое имя для короткой ссылки'


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_link(short):
    return jsonify(
        {'url': URLMap.validation_for_404(short)}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса',
                              HTTPStatus.BAD_REQUEST)
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!',
                              HTTPStatus.BAD_REQUEST)
    urlmap = URLMap()
    custom_id = data.get('custom_id')
    if not custom_id or custom_id is None:
        custom_id = URLMap.get_unique_short_id()
        data.update({'custom_id': custom_id})
    if not CUSTOM_REGEXP_ID_MODEL.match(custom_id):
        raise InvalidAPIUsage(INVALID_NAME, HTTPStatus.BAD_REQUEST)
    if not re.search(CUSTOM_REGEXP,
                     custom_id) or len(custom_id) > MIDDL_LENGTH:
        raise InvalidAPIUsage(INVALID_NAME, HTTPStatus.BAD_REQUEST)
    if URLMap.check_unique_short_id(custom_id):
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.',
            HTTPStatus.BAD_REQUEST)
    urlmap.from_dict(data)
    URLMap.save_db(urlmap)
    return jsonify(urlmap.to_dict()), HTTPStatus.CREATED
