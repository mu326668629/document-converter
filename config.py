import os

from flask import Flask
from flask_mail import Mail
from flask_errormail import mail_on_500


class ENVIRONMENT:
    development = 'development'
    production = 'production'

ADMINSTRATORS = (
    'vedarth@aplopio.com',
    'ravi@aplopio.com')

DEBUG = False
ENV = os.environ.get('APP_ENVIRONMENT', ENVIRONMENT.development)

UPLOAD_FOLDER = 'tmp/'
OUTPUT_FOLDER = 'output/'

S3_BUCKET = os.environ.get('S3_BUCKET')
REMOTE_INPUT_FOLDER = 'input'
REMOTE_DUMP_FOLDER = 'output'
POSTGRES_DB_URI = os.environ.get('POSTGRES_DB_URI')
HEARTBEAT_URL = os.environ.get('HEARTBEAT_URL', 'heartbeat')

SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')

ALLOWED_EXTENSIONS = ['pdf', 'txt', 'html', 'doc', 'docx']

LIBRE_OFFICE_HOST = '127.0.0.1'
LIBRE_OFFICE_PORT = '2220'

LOGENTRIES_KEY = os.environ.get('LOGENTRIES_KEY', '')


app = Flask(__name__)
mail = Mail(app)
mail_on_500(app, ADMINSTRATORS)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config.from_object(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = app.config['POSTGRES_DB_URI']
