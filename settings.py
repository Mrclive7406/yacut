import os
import re
import string

MAX_TRIES = 10
MAX_SHORT_LENGTH = 16
MAX_URL_LENGTH = 2048
MAX_GENERATED_SHORT_LENGTH = 6
ALPHANUMERIC_CHARACTERS = string.ascii_letters + string.digits
SHORT_REGEXP = f'^[{re.escape(ALPHANUMERIC_CHARACTERS)}]+$'
CUSTOM_ID_REGEXP_COMPILED = re.compile(SHORT_REGEXP)
GET_SHORT_URL_ENDPOINT_NAME = 'get_short_url'


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
    SECRET_KEY = os.getenv('SECRET_KEY')
