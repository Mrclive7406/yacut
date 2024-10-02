
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (DataRequired, Optional, Regexp, Length, URL)

from settings import (CUSTOM_REGEXP, MAX_ORIGINAL_LINK_LENGHT,
                      MIN_LENGTH_CUSTOM, CUSTOM_MIDDL_LENGTH)


class UrlForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(MIN_LENGTH_CUSTOM, MAX_ORIGINAL_LINK_LENGHT,
                   message='Длинна поля от 1 до 256 символов'),
            URL(message='Некорректная ссылка')
        ])
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(MIN_LENGTH_CUSTOM, CUSTOM_MIDDL_LENGTH,
                   message='Длинна поля от 1 до 16 символов'),
            Optional(),
            Regexp(
                CUSTOM_REGEXP,
                message='Указано недопустимое имя для короткой ссылки'
                        'Для ссылки допустимы символы латинского '
                        'алфавита и цифры от 0 до 9.')
        ])
    submit = SubmitField('Создать')
