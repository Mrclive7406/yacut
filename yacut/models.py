import random
import re
from http import HTTPStatus

from datetime import datetime

from flask import url_for

from settings import (MAX_LENGHT, MIDDL_LENGTH,
                      LATTER_AND_DIGITS, MAX_GENERATED_LENGTH,
                      CUSTOM_REGEXP_ID_MODEL,
                      LATTER_AND_DIGITS, CUSTOM_REGEXP)
from .error_handlers import InvalidAPIUsage
from yacut import db


INVALID_NAME = 'Указано недопустимое имя для короткой ссылки'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LENGHT), nullable=False)
    short = db.Column(db.String(MIDDL_LENGTH), unique=True,
                      nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def from_dict(self, data):
        self.original = data.get('url')
        self.short = data.get('custom_id')

    def to_dict(self):
        return {
            'url': self.original,
            'short_link': url_for('get_short_url', url_short=self.short,
                                  _external=True)
        }

    @classmethod
    def check_unique_short_id(cls, short):
        return cls.query.filter_by(short=short).first() is not None

    @classmethod
    def get_unique_short_id(cls):
        while True:
            rand_string = ''.join(random.sample(LATTER_AND_DIGITS,
                                                MAX_GENERATED_LENGTH))
            if not cls.check_unique_short_id(rand_string):
                return rand_string

    @classmethod
    def get_short_url_or_404(cls, url_short):
        return cls.query.filter_by(short=url_short).first_or_404()

    @staticmethod
    def save_db(data):
        db.session.add(data)
        db.session.commit()

    @classmethod
    def validatator_custom_id(cls, data):
        custom_id = data.get('custom_id')
        if not custom_id or custom_id is None:
            custom_id = cls.get_unique_short_id()
            data.update({'custom_id': custom_id})
        if not CUSTOM_REGEXP_ID_MODEL.match(custom_id):
            raise InvalidAPIUsage(INVALID_NAME, HTTPStatus.BAD_REQUEST)
        return custom_id

    @classmethod
    def is_short_id_exists(cls, short_id):
        return cls.query.filter_by(short=short_id).first() is not None

    @classmethod
    def create_entry(cls, original, short):
        link = cls(original=original, short=short)
        db.session.add(link)
        db.session.commit()
        return link

    @staticmethod
    def validation_for_404(url_short):
        url = URLMap.query.filter_by(short=url_short).first()
        if not url:
            raise InvalidAPIUsage('Указанный id не найден',
                                  HTTPStatus.NOT_FOUND)
        return url.original

    @staticmethod
    def short_id_validater(short_id):
        if not re.search(CUSTOM_REGEXP,
                         short_id) or len(short_id) > MIDDL_LENGTH:
            raise InvalidAPIUsage('Указано недопустимое имя для короткой'
                                  ' ссылки', HTTPStatus.BAD_REQUEST)
        if URLMap.query.filter_by(short=short_id).first():
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.',
                HTTPStatus.BAD_REQUEST)
