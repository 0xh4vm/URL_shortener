import os
from datetime import timedelta


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = True
    SECRET_KEY = 'gwkghkf2934ysfljb45efsjfhkadslg2'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/url_shortener'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Test(object):
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'gwkghkf2934ysfljb45efsjfhkadslg2'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/test_url_shortener'
    SQLALCHEMY_TRACK_MODIFICATIONS = False