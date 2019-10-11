import os
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    # DB_USERNAME = os.environ.get('DB_USERNAME')
    # DB_PASSWORD = os.environ.get('DB_PASSWORD')
    # SQLALCHEMY_DATABASE_URI='mysql+pymysql:///$PWD/Dashgang.sql'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'+DB_USERNAME+':'+DB_PASSWORD+'@146.118.64.10/Dashgang'
    PW = os.environ.get('DB_PASSWORD')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:'+PW+'@localhost/Dashgang'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ['SECRET_KEY']
    # MYSQL_HOST = localhost
    # MYSQL_USER = root
    # MYSQL_PASSWORD = os.environ.get('DB_PASSWORD')
    # MYSQL_DB = Dashgang
