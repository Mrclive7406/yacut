
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

from settings import (SHORT_REGEXP, MAX_URL_LENGTH,
                      MAX_SHORT_LENGTH)

LONG_LINK = 'Длинная ссылка'
REQUIRED_FIELD = 'Обязательное поле'
ORIGINAL_LENGTH_MESSAGE = f'Длинна поля от 1 до {MAX_URL_LENGTH}'
INVALID_LINK = 'Некорректная ссылка'
SHORT = 'Ваш вариант короткой ссылки'
SHORT_LENGTH_MESSAGE = f'Длинна поля от 1 до {MAX_SHORT_LENGTH} символов'
REGEXP_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
SUBMIT = 'Создать'


class UrlForm(FlaskForm):
    original_link = URLField(LONG_LINK, validators=[DataRequired(
        message=REQUIRED_FIELD),
        Length(max=MAX_URL_LENGTH, message=ORIGINAL_LENGTH_MESSAGE),
        URL(message=INVALID_LINK)])
    custom_id = StringField(
        SHORT,
        validators=[
            Length(max=MAX_SHORT_LENGTH,
                   message=SHORT_LENGTH_MESSAGE),
            Optional(),
            Regexp(
                SHORT_REGEXP,
                message=REGEXP_MESSAGE)
        ])
    submit = SubmitField(SUBMIT)
