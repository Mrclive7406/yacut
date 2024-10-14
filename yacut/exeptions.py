from http import HTTPStatus 
 
from flask import jsonify 
 
from . import app 
 
 
class ValidationError(Exception): 
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY 
 
    def __init__(self, message, status_code=None): 
        super().__init__() 
        self.message = message 
        if status_code is not None: 
            self.status_code = status_code 
 
    def to_dict(self): 
        return dict(message=self.message) 
 
 
@app.errorhandler(ValidationError) 
def validation_error(error): 
    return jsonify(error.to_dict()), error.status_code