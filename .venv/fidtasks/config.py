import os

class Config:
    # secret key for csrf
    SECRET_KEY = '484cf8d93e56f8d6e7b6d9efeba11dc4'

    # for sql database definition
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    