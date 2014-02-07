import os
import re
from utils import *
from config import app, db
from models import File, Conversion, Account, STATUS, PRIORITY
from semisync import semisync
from time import sleep, time
from tasks import document_converter
from file_manager import get_signed_url, upload_to_remote

from flask import abort, request, jsonify, g, url_for
from werkzeug import secure_filename
from flask.ext.httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = Account.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = Account.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

@app.route('/api/users', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    callback = request.json.get('callback')
    if username is None or password is None:
        abort(400) # missing arguments
    if Account.query.filter_by(username = username).first() is not None:
        abort(400) # existing user
    user = Account(username = username)
    user.hash_password(password)
    user.callback = callback
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': user.username }), 201, \
        {'Location': url_for('get_user', id = user.id, _external = True)}

@app.route('/api/users/<int:id>')
def get_user(id):
    user = Account.query.get(id)
    if not user:
        abort(400)
    return jsonify({ 'username': user.username })

@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(3153600000)
    return jsonify({ 'token': token.decode('ascii'), 'duration': 3153600000 })

@app.route('/upload', methods = ['POST'])
@auth.login_required
def upload():
    # Get priority
    priority = int(request.form.get('priority', PRIORITY.medium))
    if priority not in PRIORITY.get_values():
        priority = PRIORITY.medium

    # Get output formats
    output_formats = request.form.get('output-formats', '')
    output_formats = list(set(
        filter(
            lambda format: format in app.config['ALLOWED_EXTENSIONS'],
            output_formats.split(';')
        )
    ))
    if not output_formats:
        return jsonify({'Error': 'Must provide valid output formats'}), 400

    # Get file (either directly or via URL)
    file = request.files.get('file')
    allowed_extensions = app.config['ALLOWED_EXTENSIONS']
    if file:
        if allowed_filename(file.filename, allowed_extensions):
            filename = secure_filename(file.filename)
            local_path = os.path.join(app.config['UPLOAD_FOLDER'],
                timestamp_filename(filename))
            file.save(local_path)
        else:
            return jsonify({'Error': 'File format not allowed'}), 400
    else:
        fileURL = request.form.get('fileURL')
        if fileURL:
            filename = get_filename_from_url(fileURL)
            local_path = download_url(fileURL, app.config['UPLOAD_FOLDER'], timestamp = True)
        else:
            return jsonify({'Error': 'File seems screwed'}), 400
    
    # Upload to remote and remove file from local
    remote_destination = os.path.join(app.config['REMOTE_INPUT_FOLDER'],
        get_uuid(), filename)
    upload_to_remote(remote_destination, local_path)
    os.remove(local_path)

    # Register the file for conversions and return docIds
    docIds = Conversion.register_file(filename, remote_destination, g.user, output_formats, priority)
    return jsonify({'Status': STATUS.introduced, 'docIds': docIds})

@app.route('/download', methods = ['POST'])
@auth.login_required
def download():
    docId = request.json.get('docId')
    conversion = Conversion.get_by_doc_id(docId, g.user.id)
    if conversion and conversion.status == STATUS.completed:
        filename = rename_filename_with_extension(conversion.file_instance.filename,
            conversion.output_format)
        remote_location = os.path.join(app.config['REMOTE_DUMP_FOLDER'], conversion.doc_id, 
            filename)
    
        return jsonify({'Signed URL': get_signed_url(remote_location), 'docId': docId}), 200
    return jsonify({'Error': 'Failed to get conversion'}), 404

@app.route('/dummy_callback', methods = ['POST'])
def dummy_callback():
    print request.data
    return jsonify({'success': 'ok'})

def output():
    pass

@semisync(callback = output)
def request_fetcher(pm = PidManager('proc/rf.pid')):
    pm.register()
    while True:
        # Get conversions by priority
        conversions = Conversion.get_requests_by_priority(limit = 1)

        # Forward request ids to document converter
        conversion_ids = map(lambda conversion: conversion.id, conversions)
        if conversion_ids:
            document_converter.delay(conversion_ids)

            # Mark Queued
            for conversion in conversions:
                conversion.status = STATUS.queued
                db.session.commit()

        # Iter after sleep
        sleep(0.2)

@semisync(callback = output)
def app_server():
    app.run()

if __name__ == '__main__':
    rf = PidManager('proc/rf.pid')
    
    if not rf.is_running():
        request_fetcher(rf)

    app_server()
    semisync.begin()