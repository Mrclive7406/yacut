import os
import re

MIN_LENGTH_CUSTOM_ID = 1
CUSTOM_ID_MIDDL_LENGTH = 16
MAX_ORIGINAL_LINK_LENGHT = 256
MAX_GENERATED_LENGTH = 6
CUSTOM_REGEXP = '^[a-zA-Z0-9]*'
CUSTOM_REGEXP_ID = fr"[a-zA-Z0-9]{{{MIN_LENGTH_CUSTOM_ID},{CUSTOM_ID_MIDDL_LENGTH}}}$"
CUSTOM_REGEXP_ID_MODEL = re.compile(CUSTOM_REGEXP_ID)
URL = 'url'
CUSTOM_ID = 'custom_id'
MAIN_PAGE_TEMPLATE = 'index.html'
TEMPLATE_404 = 'core/404.html'
TEMPLATE_500 = 'core/500.html'
MAIN_URL = '/'
API_GET_URL = '/api/id/<string:url_short>/'
API_POST_URL = '/api/id/'
STRING_URL_SHORTS = '/<string:url_short>'


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')