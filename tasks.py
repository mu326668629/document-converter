import os
import json
from utils import rename_filename_with_extension, get_extension_from_filename
from celery import Celery
import requests

JSON_HEADERS = {'Content-type': 'application/json', 'Accept': 'application/json'}

from config import db
from config import app as flask_app
from models import Account, File, Conversion, STATUS

from converters.document_converter import convert
from file_manager import FileManager

db.create_scoped_session()

BROKER_URL = 'redis://localhost:6379/0'
app = Celery('tasks', broker=BROKER_URL)

@app.task
def document_converter(request_ids):
    # Get all conversion requests.
    for request_id in request_ids:
        conversion = Conversion.query.get(request_id)

        # Request callback
        callback = conversion.file_instance.account_instance.callback
        
        # POST: informing QUEUED
        post_handler.delay(callback, {
            'Status': conversion.status,
            'docId': conversion.doc_id
            }
        )

        # Convert document.
        inputFilePath = os.path.join(flask_app.config['UPLOAD_FOLDER'],
                                conversion.file_instance.location)

        fm = FileManager(inputFilePath, flask_app.config['OUTPUT_FOLDER'])
        convert([fm], [conversion.output_format])

        if fm.is_converted():
            print conversion.file_instance, "The file was converted successfully"
            
            conversion.status = STATUS.converted
            db.session.commit()
            
            # Post status to callback
            post_handler.delay(callback, {
                'Status': conversion.status,
                'docId': conversion.doc_id
                }
            )
            # Spawn off upload
            extension = get_extension_from_filename(fm.get_output_file_path())
            destination_filename = rename_filename_with_extension(
                conversion.file_instance.filename, extension)

            destination = os.path.join(flask_app.config['S3_DUMP_FOLDER'],
                conversion.doc_id, destination_filename)
            fm.set_remote_destination(destination)
            remote_upload_handler.delay(fm, conversion.id)
        else:
            print "Unable to convert file"
            
            conversion.status = STATUS.failed
            db.session.commit()

            post_handler.delay(callback, {
                'Status': conversion.status,
                'docId': conversion.doc_id
                }
            )

@app.task
def post_handler(url, data):
    requests.post(url, data=json.dumps(data), headers=JSON_HEADERS)

@app.task
def remote_upload_handler(file_manager_obj, conversion_id):
    conversion = Conversion.query.get(conversion_id)
    callback = conversion.file_instance.account_instance.callback
    output_file_signed_url = file_manager_obj.upload_output_file()
    conversion.signed_url = output_file_signed_url
    conversion.status = STATUS.completed
    db.session.commit()

    # POST signed URL with status and doc_id
    post_handler.delay(callback, {
        'Status': conversion.status,
        'Signed URL': conversion.signed_url,
        'docId': conversion.doc_id
        }
    )   