import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ['SECRET_KEY']
    ALLOWED_HOSTS = ['0.0.0.0', 'localhost', 'https://flaskdash-deployment-test.herokuapp.com/']
       