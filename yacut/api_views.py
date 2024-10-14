from http import HTTPStatus
from collections import namedtuple

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap

INVALID_NAME = 'Указано недопустимое имя для короткой ссылки'
MISSING_BODY_REQUEST = 'Отсутствует тело запроса'
URL_REQUIRED_FIELD = '"url" является обязательным полем!'
MODEL_FIELDS = namedtuple('Fields', ['id', 'original', 'short', 'timestamp'])
REQUEST_FIELDS = MODEL_FIELDS(None, 'url', 'custom_id', None)


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_link(short):
    if not (url_map := URLMap.get(short)):
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original})


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage(MISSING_BODY_REQUEST,
                              HTTPStatus.BAD_REQUEST)
    original = data.get(REQUEST_FIELDS.original)
    if not original:
        raise InvalidAPIUsage(URL_REQUIRED_FIELD,
                              HTTPStatus.BAD_REQUEST)
    try:
        return jsonify(
            URLMap.create_entry(original,
                                data.get(REQUEST_FIELDS.short)).to_dict()
        ), HTTPStatus.CREATED
    except (ValueError) as error:
        raise InvalidAPIUsage(str(error))
