import requests
import json

__all__ = ['create_user', 'get_auth_token', 'upload_file', 'upload_via_url', 'download']

# Change it to the location where doc converter is hosted
BASE_URL = 'http://127.0.0.1:5000'

JSON_POST_HEADERS = {
    'Content-type': 'application/json',
    'Accept': 'application/json'
}

def get_auth_obj_for_token(auth_token):
    if type(auth_token) is dict:
        auth_token = auth_token['token']
    return requests.auth.HTTPBasicAuth(auth_token, 'unsed')

def create_user(username, password, callback):
    credentials = {
        'username': username,
        'password': password,
        'callback': callback
    }
    r = requests.post(BASE_URL + '/api/users',
            data = json.dumps(credentials),
            headers = JSON_POST_HEADERS
        )
    if r.status_code < 400:
        return r.json()

def get_auth_token(username, password):
    auth_obj = requests.auth.HTTPBasicAuth(username, password)
    r = requests.get(BASE_URL + '/api/token',
            headers = {'Accept': "application/json"},
            auth=auth_obj)
    return r.json()

def upload_file(auth_token, filepath, output_formats, priority):
    auth_obj = get_auth_obj_for_token(auth_token)
    r = requests.post(BASE_URL + '/upload',
        data = {
            'priority': priority,
            'output-formats': output_formats
        },
        files = {'file': open(filepath, 'rb')},
        headers = {'Accept': "application/json"},
        auth = auth_obj)
    return r.json()

def upload_via_url(auth_token, fileURL, output_formats, priority):
    auth_obj = get_auth_obj_for_token(auth_token)
    r = requests.post(BASE_URL + '/upload',
        data = {
            'fileURL': fileURL,
            'priority': priority,
            'output-formats': output_formats
        },
        headers = {'Accept': "application/json"},
        auth = auth_obj)
    return r.json()

def download(auth_token, docId):
    auth_obj = get_auth_obj_for_token(auth_token)
    r = requests.post(BASE_URL + '/download',
        data = json.dumps({
            'docId': docId
        }),
        headers = JSON_POST_HEADERS,
        auth = auth_obj)
    return r.json()