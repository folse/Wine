import os

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'tell u the seqcret'
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
MAIL_SERVER = 'smtp.ym.163.com'
MAIL_PORT = 25
MAIL_USE_TLS = True
MAIL_USERNAME = 'no-reply@bxzz.net'
MAIL_PASSWORD = 'getBxzz@2015'
MAIL_SUBJECT_PREFIX = '[Zhiyou]'
MAIL_SENDER = 'Zhiyou <no-reply@bxzz.net>'
CUSTOMERS_PER_PAGE = 10

DEBUG = True
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:makeFuture@localhost/wine'
