import os
import re
from string import ascii_letters, digits

MAX_URL_TRIES = 5
MAX_CUSTOM_ID_LENGTH = 16
MAX_URL_LENGTH = 2048
MAX_GENERATED_ID_LENGTH = 6
CUSTOM_REGEXP = r'^[a-zA-Z\d]{1,16}$'
CUSTOM_ID_REGEXP_COMPILED = re.compile(CUSTOM_REGEXP)
ALPHANUMERIC_CHARACTERS = ascii_letters + digits
GET_SHORT_URL_ENDPOINT_NAME = 'get_short_url'


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
    SECRET_KEY = os.getenv('SECRET_KEY')
