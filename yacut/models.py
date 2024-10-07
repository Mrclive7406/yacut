import random
import re
from datetime import datetime
from http import HTTPStatus

from flask import url_for

from settings import (ALPHANUMERIC_CHARACTERS, CUSTOM_REGEXP,
                      GET_SHORT_URL_ENDPOINT_NAME, MAX_CUSTOM_ID_LENGTH,
                      MAX_GENERATED_ID_LENGTH, MAX_URL_LENGTH, MAX_URL_TRIES)
from yacut import db

from .error_handlers import InvalidAPIUsage

INVALID_NAME = 'Указано недопустимое имя для короткой ссылки'
LINK_EXICTS = 'Предложенный вариант короткой ссылки уже существует.'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_URL_LENGTH), nullable=False)
    short = db.Column(db.String(MAX_CUSTOM_ID_LENGTH), unique=True,
                      nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return {
            'url': self.original,
            'short_link': url_for(GET_SHORT_URL_ENDPOINT_NAME,
                                  url_short=self.short,
                                  _external=True)
        }

    @staticmethod
    def check_unique_short_id(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_unique_short_id():
        for _ in range(MAX_URL_TRIES):
            rand_string = ''.join(random.sample(ALPHANUMERIC_CHARACTERS,
                                                MAX_GENERATED_ID_LENGTH))
            if not URLMap.check_unique_short_id(rand_string):
                return rand_string

    @staticmethod
    def find_obj_or_404(url_short):
        return URLMap.query.filter_by(short=url_short).first_or_404()

    @staticmethod
    def save_db(data):
        custom_id = data.get('custom_id')
        if not custom_id:
            custom_id = URLMap.get_unique_short_id()
            data.update({'custom_id': custom_id})
        if not re.search(CUSTOM_REGEXP,
                         custom_id) or len(custom_id) > MAX_CUSTOM_ID_LENGTH:
            raise InvalidAPIUsage(INVALID_NAME, HTTPStatus.BAD_REQUEST)
        if URLMap.check_unique_short_id(custom_id):
            raise InvalidAPIUsage(LINK_EXICTS, HTTPStatus.BAD_REQUEST)
        urlmap = URLMap(original=data['url'], short=custom_id)
        db.session.add(urlmap)
        db.session.commit()
        return urlmap

    @staticmethod
    def is_short_id_exists(custom_id):
        return URLMap.check_unique_short_id(custom_id)

    @staticmethod
    def validation_for_404(url_short):
        url = URLMap.query.filter_by(short=url_short).first()
        if not url:
            raise InvalidAPIUsage('Указанный id не найден',
                                  HTTPStatus.NOT_FOUND)
        return url.original

    @staticmethod
    def create_entry(original, short=None):
        if short is None:
            short = URLMap.get_unique_short_id()
        if URLMap.is_short_id_exists(short):
            return None, HTTPStatus.BAD_REQUEST
        link = URLMap(original=original, short=short)
        db.session.add(link)
        db.session.commit()
        short_url = url_for('get_short_url',
                            url_short=short, _external=True)
        return link, short_url
