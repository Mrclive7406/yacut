
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

from settings import (MIDDL_LENGTH, CUSTOM_REGEXP,
                      MAX_LENGHT,)


LONG_LINK = 'Длинная ссылка'
REQUIRED_FIELD = 'Обязательное поле'
ORIGINAL_LENGTH_MESSAGE = 'Длинна поля от 1 до {MAX_ORIGINAL_LINK_LENGHT}'
' символов'
INVALID_LINK = 'Некорректная ссылка'
SHORT_LINK_OPTION = 'Ваш вариант короткой ссылки'
CUSTOM_LENGTH_MESSAGE = 'Длинна поля от 1 до {CUSTOM_MIDDL_LENGTH} символов'
REGEXP_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
'Для ссылки допустимы символы латинского '
'алфавита и цифры от 0 до 9.'
SUBMIT = 'Создать'


class UrlForm(FlaskForm):
    original_link = URLField(LONG_LINK, validators=[DataRequired(
        message=REQUIRED_FIELD),
        Length(1, MAX_LENGHT, message=ORIGINAL_LENGTH_MESSAGE),
        URL(message=INVALID_LINK)])
    custom_id = StringField(
        SHORT_LINK_OPTION,
        validators=[
            Length(1, MIDDL_LENGTH,
                   message=CUSTOM_LENGTH_MESSAGE),
            Optional(),
            Regexp(
                CUSTOM_REGEXP,
                message=REGEXP_MESSAGE)
        ])
    submit = SubmitField(SUBMIT)
