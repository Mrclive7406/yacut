from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap

INVALID_NAME = 'Указано недопустимое имя для короткой ссылки'


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_link(short):
    return jsonify(
        {'url': URLMap.verify_record_for_404(short)}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса',
                              HTTPStatus.BAD_REQUEST)
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!',
                              HTTPStatus.BAD_REQUEST)
    urlmap = URLMap.save_db(data)
    return jsonify(urlmap.to_dict()), HTTPStatus.CREATED
