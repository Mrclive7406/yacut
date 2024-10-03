import os
import re
from string import ascii_letters, digits


MIDDL_LENGTH = 16
MAX_LENGHT = 2048
MAX_GENERATED_LENGTH = 6
CUSTOM_REGEXP = '[a-zA-Z0-9]'
CUSTOM_REGE_ID = fr"{CUSTOM_REGEXP}{{1,{MIDDL_LENGTH}}}$"
CUSTOM_REGEXP_ID_MODEL = re.compile(CUSTOM_REGE_ID)
GET_SHORT_URL = 'get_short_url'
LATTER_AND_DIGITS = ascii_letters + digits


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
    SECRET_KEY = os.getenv('SECRET_KEY')
