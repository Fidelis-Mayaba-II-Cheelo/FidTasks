import os

class Config:
    # secret key for csrf
    SECRET_KEY = os.environ,get('SECRET_KEY')

    # for sql database definition
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    