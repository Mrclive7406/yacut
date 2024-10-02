from datetime import datetime
from flask import url_for
from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def from_dict(self, data):
        self.original = data.get('url')
        self.short = data.get('custom_id')

    def to_dict(self):
        return {
            'url': self.original,
            'short_link': url_for('get_short_url', url_short=self.short,
                                  _external=True)
        }