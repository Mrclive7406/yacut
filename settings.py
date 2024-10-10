import os
import re
import string

MAX_URL_TRIES = 5
MAX_SHORT_LENGTH = 16
MAX_URL_LENGTH = 2048
MAX_GENERATED_SHORT_LENGTH = 6
SHORT_REGEXP = r'^[a-zA-Z\d]{1,16}$'
CUSTOM_ID_REGEXP_COMPILED = re.compile(SHORT_REGEXP)
ALPHANUMERIC_CHARACTERS = string.ascii_letters + string.digits
GET_SHORT_URL_ENDPOINT_NAME = 'get_short_url'


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
    SECRET_KEY = os.getenv('SECRET_KEY')
