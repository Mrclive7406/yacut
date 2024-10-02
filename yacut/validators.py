from .error_handlers import InvalidAPIUsage
from .models import URLMap
import random
import re
from settings import (URL, MAX_GENERATED_LENGTH,
                      CUSTOM_REGEXP, CUSTOM_ID_MIDDL_LENGTH)
from .error_handlers import InvalidAPIUsage
from string import ascii_letters, digits
from http import HTTPStatus


def get_unique_short_id():
    letters_and_digits = ascii_letters + digits
    rand_string = ''.join(random.sample(letters_and_digits,
                                        MAX_GENERATED_LENGTH))
    if not URLMap.query.filter_by(short=rand_string).first():
        return rand_string


def validation_for_404(url_short):
    url = URLMap.query.filter_by(short=url_short).first()
    if not url:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return url.original


def validation_data(data):
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса',
                              HTTPStatus.BAD_REQUEST)
    if URL not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!',
                              HTTPStatus.BAD_REQUEST)


def short_id_validater(short_id):
    if not re.search(CUSTOM_REGEXP,
                     short_id) or len(short_id) > CUSTOM_ID_MIDDL_LENGTH:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки',
                              HTTPStatus.BAD_REQUEST)
    if URLMap.query.filter_by(short=short_id).first():
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.',
            HTTPStatus.BAD_REQUEST)