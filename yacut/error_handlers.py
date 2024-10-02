from flask import jsonify, render_template

from settings import TEMPLATE_404, TEMPLATE_500
from . import app, db
from http import HTTPStatus


class InvalidAPIUsage(Exception):
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error):
    return render_template(TEMPLATE_404), HTTPStatus.NOT_FOUND


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_error(error):
    db.session.rollback()
    return render_template(TEMPLATE_500), HTTPStatus.INTERNAL_SERVER_ERROR
