from flask import jsonify, request
from http import HTTPStatus
from . import app, db
from settings import (API_POST_URL, API_GET_URL,
                      URL, CUSTOM_ID)
from .models import URLMap
from .validators import (get_unique_short_id, validation_for_404,
                         validation_data, short_id_validater)


@app.route(API_GET_URL, methods=['GET'])
def get_original_link(url_short):
    return jsonify({URL: validation_for_404(url_short)}), HTTPStatus.OK


@app.route(API_POST_URL, methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)
    validation_data(data)
    url = URLMap()
    custom_id = data.get(CUSTOM_ID, None)
    if not custom_id or custom_id is None:
        custom_id = get_unique_short_id()
        data.update({CUSTOM_ID: custom_id})
    short_id_validater(custom_id)
    url.from_dict(data)
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), HTTPStatus.CREATED