from http import HTTPStatus

from flask import jsonify, request

from . import app
from settings import MAX_SHORT_LENGTH
from .error_handlers import InvalidAPIUsage
from .models import URLMap, MaxAttemptsExceededError

NOT_FOUND_ID = 'Указанный id не найден'
INVALID_NAME = 'Указано недопустимое имя для короткой ссылки'
MISSING_BODY_REQUEST = 'Отсутствует тело запроса'
URL_REQUIRED_FIELD = '"url" является обязательным полем!'
LINK_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_link(short):
    if not (url_map := URLMap.get(short)):
        raise InvalidAPIUsage(NOT_FOUND_ID, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original})


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage(MISSING_BODY_REQUEST,
                              HTTPStatus.BAD_REQUEST)
    original = data.get('url')
    if not original:
        raise InvalidAPIUsage(URL_REQUIRED_FIELD,
                              HTTPStatus.BAD_REQUEST)
    custom_id = data.get('custom_id')
    if custom_id:
        if len(custom_id) > MAX_SHORT_LENGTH:
            raise InvalidAPIUsage(INVALID_NAME)
    try:
        return jsonify(
            URLMap.create(original, data.get('custom_id')).to_dict()
        ), HTTPStatus.CREATED
    except ValueError as error:
        str(error) == INVALID_NAME
        raise InvalidAPIUsage(str(error), HTTPStatus.BAD_REQUEST)
    except MaxAttemptsExceededError as error:
        raise InvalidAPIUsage({str(error) == LINK_EXISTS or LINK_EXISTS},
                              HTTPStatus.BAD_REQUEST)
