import os
import json
from utils import rename_filename_with_extension, get_extension_from_filename
from file_manager import get_signed_url
from celery import Celery
import requests
from time import sleep

JSON_HEADERS = {
    'Content-type': 'application/json',
    'Accept': 'application/json'
}

from models import db
from models import Account, File, Conversion, STATUS

from converters.document_converter import convert
from file_manager import FileManager

db.create_scoped_session()

BROKER_URL = 'redis://localhost:6379/0'
app = Celery('tasks', broker=BROKER_URL)

TEXT_STATUS = {
    STATUS.introduced : 'introduced',
    STATUS.queued : 'queued',
    STATUS.converted : 'converting',
    STATUS.completed : 'completed',
    STATUS.failed : 'failed',
}


@app.task
def request_fetcher():
    # Get conversions by priority
    conversions = Conversion.get_requests_by_priority()

    # Forward request ids to document converter
    conversion_ids = map(lambda conversion: conversion.id, conversions)

    if conversion_ids:
        document_converter.delay(conversion_ids)

        # Mark Queued
        for conversion in conversions:
            conversion.status = STATUS.queued
            db.session.commit()

@app.task
def document_converter(request_ids):
    # Get all conversion requests.
    for request_id in request_ids:
        conversion = Conversion.query.get(request_id)
        # Request callback
        callback = conversion.file_instance.account_instance.callback

        # POST: informing QUEUED
        post_handler.delay(callback, {
            'status': TEXT_STATUS[conversion.status],
            'doc_id': conversion.doc_id
            }
        )

        # Convert document.
        fm = FileManager(conversion.file_instance.location)
        convert([fm], conversion.output_format)

        if fm.is_converted():
            #print conversion, "The file was converted successfully"

            conversion.status = STATUS.converted
            db.session.commit()

            # Post status to callback
            post_handler.delay(callback, {
                'status': TEXT_STATUS[conversion.status],
                'doc_id': conversion.doc_id
                }
            )
            # Spawn off upload
            remote_upload_handler.delay(fm, conversion.id)
        else:
            #print "Unable to convert file"

            conversion.status = STATUS.failed
            db.session.commit()

            post_handler.delay(callback, {
                'status': TEXT_STATUS[conversion.status],
                'doc_id': conversion.doc_id
                }
            )

@app.task
def post_handler(url, data):
    requests.post(url, data=json.dumps(data))# headers=JSON_HEADERS)
    request_fetcher.delay()

@app.task
def remote_upload_handler(file_manager_obj, conversion_id):
    conversion = Conversion.query.get(conversion_id)
    #print conversion
    callback = conversion.file_instance.account_instance.callback

    file_manager_obj.set_remote_destination(conversion.get_remote_location())
    file_manager_obj.upload_output_file()
    file_manager_obj.remove_output_file()

    conversion.status = STATUS.completed
    db.session.commit()

    conversion_siblings = conversion.get_siblings()
    output = []

    output = [get_dictionary_request(conversion) for conversion in conversion_siblings]
    post_handler.delay(callback, output)


def get_dictionary_request(conversion):
    return {
        'status': TEXT_STATUS[conversion.status],
        'signed_url': get_signed_url(conversion.get_remote_location()),
        'doc_id': conversion.doc_id,
    }
