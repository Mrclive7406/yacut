import random
from datetime import datetime
from re import search

from flask import url_for

from settings import (ALPHANUMERIC_CHARACTERS, GET_SHORT_URL_ENDPOINT_NAME,
                      MAX_GENERATED_SHORT_LENGTH, MAX_SHORT_LENGTH, MAX_TRIES,
                      MAX_URL_LENGTH, SHORT_REGEXP)
from yacut import db


ERROR_GENERATION = 'Не удалось сгенерировать уникальный уникальный ID'
INVALID_NAME = 'Указано недопустимое имя для короткой ссылки'
LINK_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'


class MaxAttemptsExceededError(Exception):
    """Исключение, превышение максимального числа попыток"""


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_URL_LENGTH), nullable=False)
    short = db.Column(db.String(MAX_SHORT_LENGTH), unique=True,
                      nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return {
            'url': self.original,
            'short_link': self.get_short_url()
        }

    def get_short_url(self):
        """Генерирует полный URL для короткой ссылки."""
        return url_for(GET_SHORT_URL_ENDPOINT_NAME,
                       short=self.short,
                       _external=True)

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_unique_short_id():
        for _ in range(MAX_TRIES):
            rand_string = ''.join(random.choices(ALPHANUMERIC_CHARACTERS,
                                                 k=MAX_GENERATED_SHORT_LENGTH))
            if not URLMap.get(rand_string):
                return rand_string
        raise MaxAttemptsExceededError(ERROR_GENERATION)

    @staticmethod
    def get_or_404(short):
        return URLMap.query.filter_by(short=short).first_or_404()

    def check_short_id(short):
        return URLMap.get(short=short) is None

    @staticmethod
    def create(original, short=None):
        short = short or URLMap.get_unique_short_id()
        if not search(SHORT_REGEXP, short):
            raise ValueError(INVALID_NAME)
        if URLMap.get(short):
            raise ValueError(LINK_EXISTS)
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map
