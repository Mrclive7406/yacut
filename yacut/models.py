import random
import re
from datetime import datetime
from http import HTTPStatus

from flask import url_for

from settings import (ALPHANUMERIC_CHARACTERS, SHORT_REGEXP,
                      GET_SHORT_URL_ENDPOINT_NAME, MAX_SHORT_LENGTH,
                      MAX_GENERATED_SHORT_LENGTH, MAX_URL_LENGTH,
                      MAX_URL_TRIES)
from yacut import db

from .error_handlers import InvalidAPIUsage

INVALID_NAME = 'Указано недопустимое имя для короткой ссылки'
LINK_EXICTS = 'Предложенный вариант короткой ссылки уже существует.'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_URL_LENGTH), nullable=False)
    short = db.Column(db.String(MAX_SHORT_LENGTH), unique=True,
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
    def unique_short_id(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_unique_short_id():
        for _ in range(MAX_URL_TRIES):
            rand_string = ''.join(random.choices(ALPHANUMERIC_CHARACTERS,
                                                 k=MAX_GENERATED_SHORT_LENGTH))
            if not URLMap.unique_short_id(rand_string):
                return rand_string

    @staticmethod
    def get_or_404(short):
        return URLMap.query.filter_by(short=short).first_or_404()

    def retrieve_obj(item, query):
        return URLMap.query.filter(item == query)

    def check_short_id(short_id):
        return URLMap.retrieve_obj(URLMap.short, short_id).first() is None

    @staticmethod
    def save_db(data, custom_id=None):
        if 'custom_id' in data:
            custom_id = data.get('custom_id')
        if custom_id == '' or custom_id is None:
            custom_id = URLMap.get_unique_short_id()
            data['custom_id'] = custom_id
        if not re.match(SHORT_REGEXP, custom_id):
            raise InvalidAPIUsage(INVALID_NAME, HTTPStatus.BAD_REQUEST)
        if not URLMap.check_short_id(custom_id):
            raise InvalidAPIUsage(LINK_EXICTS, HTTPStatus.BAD_REQUEST)
        urlmap = URLMap(original=data['url'], short=custom_id)
        db.session.add(urlmap)
        db.session.commit()
        return urlmap

    @staticmethod
    def verify_record_for_404(short):
        url = URLMap.unique_short_id(short)
        if not url:
            raise InvalidAPIUsage('Указанный id не найден',
                                  HTTPStatus.NOT_FOUND)
        return url.original

    @staticmethod
    def create_entry(original, short=None):
        urlmap = URLMap.save_db(data={'url': original, 'custom_id': short})
        return urlmap
