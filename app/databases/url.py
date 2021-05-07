from app import db
import random
import string
from datetime import datetime


class URLAssociate(db.Model):
    __tablename__ = "url_associate"

    id = db.Column(db.Integer, primary_key=True)
    protocol = db.Column(db.String(16), nullable=False)
    long = db.Column(db.String(128), nullable=False)
    short = db.Column(db.String(16), nullable=False)
    
    banned_datetime = db.relationship('BadURL')
    
    def __init__(self, protocol, long):
        self.protocol = protocol
        self.long = long
        self.short = URLAssociate.get_short()

    @staticmethod
    def get_short():
        letters = string.ascii_lowercase + string.ascii_uppercase
        while True:
            rand_letters = random.choices(letters, k=6)
            rand_letters = "".join(rand_letters)
            short_url = URLAssociate.query.filter_by(short=rand_letters).first()
            if not short_url:
                return f"{rand_letters}"

class BadURL(db.Model):
    __tablename__ = "bad_url"

    url_id = db.Column(db.Integer, db.ForeignKey('url_associate.id'), primary_key=True)
    