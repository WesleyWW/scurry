import os

class Config:
    SECRET_KEY = '2d6d7cc921s64dcdgh8'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')  