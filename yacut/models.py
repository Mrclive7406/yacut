import random

from http import HTTPStatus
from datetime import datetime

from flask import url_for

from settings import (MAX_LENGHT, MIDDL_LENGTH,
                      LATTER_AND_DIGITS, MAX_GENERATED_LENGTH, MAX_TRIES,
                      LATTER_AND_DIGITS)
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

    @staticmethod
    def check_unique_short_id(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_unique_short_id():
        for _ in range(MAX_TRIES):
            rand_string = ''.join(random.sample(LATTER_AND_DIGITS,
                                                MAX_GENERATED_LENGTH))
            if not URLMap.check_unique_short_id(rand_string):
                return rand_string

    @staticmethod
    def find_obj_or_404(url_short):
        return URLMap.query.filter_by(short=url_short).first_or_404()

    @staticmethod
    def save_db(data):
        #urlmap = URLMap()
        #custom_id = URLMap.validatator_custom_id(data)
        #URLMap.short_id_validater(custom_id)
        #urlmap.from_dict(data)
        db.session.add(data)
        db.session.commit()

    # @staticmethod
    # def validatator_custom_id(data):
    #     custom_id = data.get('custom_id')
    #     if not custom_id or custom_id is None:
    #         custom_id = URLMap.get_unique_short_id()
    #         data.update({'custom_id': custom_id})
    #     if not CUSTOM_REGEXP_ID_MODEL.match(custom_id):
    #         raise InvalidAPIUsage(INVALID_NAME, HTTPStatus.BAD_REQUEST)
    #     return custom_id

    # @staticmethod
    # def short_id_validater(short_id):
    #     if not re.search(CUSTOM_REGEXP,
    #                      short_id) or len(short_id) > MIDDL_LENGTH:
    #         raise InvalidAPIUsage('Указано недопустимое имя для короткой'
    #                               ' ссылки', HTTPStatus.BAD_REQUEST)
    #     if URLMap.query.filter_by(short=short_id).first():
    #         raise InvalidAPIUsage(
    #             'Предложенный вариант короткой ссылки уже существует.',
    #             HTTPStatus.BAD_REQUEST)

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
    def create_entry(original, custom_id=None):
        short = custom_id or URLMap.get_unique_short_id()
        if URLMap.is_short_id_exists(custom_id):
            return None
        link = URLMap(original=original, short=short)
        db.session.add(link)
        db.session.commit()
        return link

    # @classmethod
    # def create_from_data(cls, data):
    #     custom_id = data.get('custom_id') or cls.get_unique_short_id()
    #     if not CUSTOM_REGEXP.match(custom_id):
    #         raise InvalidAPIUsage('Некорректное имя для короткой ссылки',
    #                               HTTPStatus.BAD_REQUEST)
    #     if cls.check_unique_short_id(custom_id):
    #         raise InvalidAPIUsage('Вариант короткой ссылки уже существует.',
    #                               HTTPStatus.BAD_REQUEST)

    #     urlmap = cls(original=data['url'], short=custom_id)
    #     urlmap.from_dict(data)
    #     cls.save_db(urlmap)
    #     return urlmap