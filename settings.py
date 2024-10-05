import os
import re
from string import ascii_letters, digits

MAX_TRIES = 5
MIDDL_LENGTH = 16
MAX_LENGHT = 2048
MAX_GENERATED_LENGTH = 6
CUSTOM_REGEXP = r'^[a-zA-Z\d]{1,16}$'
CUSTOM_REGEXP_ID_MODEL = re.compile(CUSTOM_REGEXP)
LATTER_AND_DIGITS = ascii_letters + digits


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
    SECRET_KEY = os.getenv('SECRET_KEY')
