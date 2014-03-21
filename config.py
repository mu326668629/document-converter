import os

from flask import Flask
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

S3_BUCKET = 'document_converter'
REMOTE_INPUT_FOLDER = 'input'
REMOTE_DUMP_FOLDER = 'output'

POSTGRES_DB_URI = 'postgresql://rbox:rbox@localhost:5432/document_converter'
SECRET_KEY = '5ryNFKc13vaz8ABzMujbxFqvTerIqwNXrunGF14P'

ALLOWED_EXTENSIONS = ['pdf', 'txt', 'html', 'doc', 'docx']

app = Flask(__name__)
mail_on_500(app, ADMINSTRATORS)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config.from_object(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = app.config['POSTGRES_DB_URI']
