import os
import json
from utils import rename_filename_with_extension, get_extension_from_filename
from celery import Celery
import requests

JSON_HEADERS = {'Content-type': 'application/json', 'Accept': 'application/json'}

from models import db
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
        fm = FileManager(conversion.file_instance.location)
        convert([fm], [conversion.output_format])

        if fm.is_converted():
            #print conversion, "The file was converted successfully"
            
            conversion.status = STATUS.converted
            db.session.commit()
            
            # Post status to callback
            post_handler.delay(callback, {
                'Status': conversion.status,
                'docId': conversion.doc_id
                }
            )
            # Spawn off upload
            fm.set_remote_destination(conversion.get_remote_location())
            remote_upload_handler.delay(fm, conversion.id)
        else:
            #print "Unable to convert file"
            
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
    #print conversion
    callback = conversion.file_instance.account_instance.callback
    output_file_url = file_manager_obj.upload_output_file()
    conversion.status = STATUS.completed
    db.session.commit()

    # POST signed URL with status and doc_id
    post_handler.delay(callback, {
        'Status': conversion.status,
        'Signed URL': output_file_url,
        'docId': conversion.doc_id
        }
    )