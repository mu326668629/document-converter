import os
import json
from file_manager import get_signed_url
from celery import Celery
import requests

JSON_HEADERS = {
    'Content-type': 'application/json',
    'Accept': 'application/json'
}

from models import db
from logger import log
from file_manager import FileManager
from models import Conversion, STATUS
from utils import log_execution_time
from converters.document_converter import convert


db.create_scoped_session()

BROKER_URL = os.environ.get('BROKER_URL')
app = Celery('tasks', broker=BROKER_URL)

TEXT_STATUS = {
    STATUS.introduced: 'introduced',
    STATUS.queued: 'queued',
    STATUS.converted: 'converting',
    STATUS.completed: 'completed',
    STATUS.failed: 'failed',
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

        if 'completed' in TEXT_STATUS[conversion.status]:
            continue

        # Request callback
        callback = conversion.file_instance.account_instance.callback

        # Convert document.
        fm = FileManager(conversion.file_instance.location)
        convert([fm], conversion.output_format)

        # POST to callback for conversion queued
        post_handler.apply_async((callback,
                                  [{
                                      'status': TEXT_STATUS[conversion.status],
                                      'doc_id': conversion.doc_id
                                  }]))

        if fm.is_converted():
            log.info('File converted conversion_to {} id={}, doc_id={}, file={}, status=success'.format(
                conversion.output_format, conversion.id, conversion.doc_id,
                conversion.file_instance.location))
            conversion.status = STATUS.converted
            db.session.commit()

            # Queue converted file for uploading
            remote_upload_handler(fm, conversion.id)
        else:
            log.error('File not converted to {}! file={}, status=failed, conversion_id={}'.format(
                conversion.output_format, conversion.file_instance.location,
                conversion.id))
            conversion.status = STATUS.failed
            db.session.commit()
            handle_conversion_completion.apply_async(
                (conversion, STATUS.failed), queue='post_handler')

    request_fetcher.delay()


@app.task
def post_handler(url, data):
    send_postback(url, data)


def remote_upload_handler(file_manager_obj, conversion_id):
    conversion = Conversion.query.get(conversion_id)
    file_manager_obj.set_remote_destination(conversion.get_remote_location())
    file_manager_obj.upload_output_file()
    log.info('Uploading file={}, conversion_id={}'.format(
        conversion.file_instance.location, conversion.id))
    file_manager_obj.remove_output_file()
    log.info('Sending postback for file={}, conversion_id={}'.format(
        conversion.file_instance.location, conversion.id))

    handle_conversion_completion.apply_async((conversion, STATUS.completed),
                                             queue='post_handler')


@app.task
def handle_conversion_completion(conversion=None, status=None):
    if not conversion or not status:
        return None

    callback = conversion.file_instance.account_instance.callback
    conversion.status = status
    db.session.commit()

    conversion_siblings = conversion.get_siblings()
    output = []

    output = [get_dictionary_request(conversion_sib)
              for conversion_sib in conversion_siblings]

    send_postback(callback, output)


@log_execution_time('get_request_dict')
def get_dictionary_request(conversion):
    return {
        'status': TEXT_STATUS[conversion.status],
        'signed_url': get_signed_url(conversion.get_remote_location()),
        'doc_id': conversion.doc_id,
    }


def send_postback(url, data):

    try:
        response = requests.post(url, data=json.dumps(data), timeout=60)
    except Exception as e:
        log.error('Postback error {}'.format(e))
        post_handler.apply_async((url, data))

    for d in data:
        log.info('Postback status {} for doc_id={}, signed_url={}'.format(
            response.status_code,
            d.get('doc_id', ''), d.get('signed_url', '')))
