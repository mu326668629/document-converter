import os
from utils import *
from config import app, db
from models import File, Conversion, Account, STATUS, PRIORITY
from semisync import semisync
from time import sleep
from tasks import document_converter

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
    priority = int(request.form.get('priority', PRIORITY.medium))
    if priority not in PRIORITY.get_values():
        priority = PRIORITY.medium

    output_formats = request.form.get('output-formats', '')
    output_formats = list(set(
        filter(
            lambda format: format in app.config['ALLOWED_EXTENSIONS'],
            output_formats.split(';')
        )
    ))
    
    if not output_formats:
        return jsonify({'Error': 'Must provide valid output formats'}, 400)

    file = request.files.get('file')
    allowed_extensions = app.config['ALLOWED_EXTENSIONS']

    if file and allowed_filename(file.filename, allowed_extensions):
        filename = secure_filename(file.filename)
        location = timestamp_filename(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], location))
    else:
        fileURL = request.form.get('fileURL')
        if fileURL:
            filename = get_filename_from_url(fileURL)
            location = download_url(fileURL, app.config['UPLOAD_FOLDER'], timestamp = True)
        else:
            return jsonify({'Error': 'File seems screwed'}, 400)
    
    docIds = Conversion.register_file(filename, location, g.user, output_formats, priority)
    return jsonify({'Status': STATUS.introduced, 'docIds': docIds})


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
        conversions = Conversion.get_requests_by_priority(limit = 3)

        # Forward request ids to document converter
        conversion_ids = map(lambda conversion: conversion.id, conversions)
        document_converter.delay(conversion_ids)

        # Mark Queued
        for conversion in conversions:
            conversion.status = STATUS.queued
            db.session.commit()

        # Iter after sleep
        sleep(0.5)

@semisync(callback = output)
def app_server():
    app.run()

if __name__ == '__main__':
    pm = PidManager('proc/rf.pid')
    if not pm.is_running():
        print "Request fetcher not running..."
        request_fetcher(pm)
    else:
        print "Request fetcher running, no need to fork..."

    app_server()
    semisync.begin()