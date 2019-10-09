import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    FLASK_APP=dashapp
    FLASK_ENV=development
    DATABASE_URL=sqlite:///$PWD/app.db
    SECRET_KEY=secret_key_change_as_you_wish_make_it_long_123
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ['SECRET_KEY']


