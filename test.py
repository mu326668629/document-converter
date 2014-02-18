import os
import time
from models import db, STATUS, PRIORITY, File, Conversion, Account
from config import app
from utils import Command
from semisync import semisync
import requests
import json

from boto.s3.connection import S3Connection
from boto.s3.key import Key

AWS_S3_CONNECTION = S3Connection()
bucket = AWS_S3_CONNECTION.get_bucket(app.config['S3_BUCKET'])

BASE_URL = 'http://127.0.0.1:8200'
JSON_POST_HEADERS = {'Content-type': 'application/json', 'Accept': 'application/json'}

# dummy_auth = requests.auth.HTTPBasicAuth(username, password)
dummy_token_auth = lambda token: requests.auth.HTTPBasicAuth(token, 'unused')

def is_ok_response(r):
    return r.status_code >= 200 and r.status_code < 400

def is_unauthorised_call(r):
    return r.status_code == 401

def call_dummy_request(dummy_request, auth_obj):
    method = dummy_request['method']
    if method == 'POST':
        if dummy_request['type'] == 'files':
            return requests.post(dummy_request['url'],
                data = dummy_request['data'],
                files = dummy_request['files'],
                headers = dummy_request['headers'],
                auth = auth_obj)
        else:
            return requests.post(dummy_request['url'],
                data = dummy_request['data'],
                headers = dummy_request['headers'],
                auth = auth_obj)
    elif method == 'GET':
        pass

class DummyRequests(object):
    def __init__(self, base_url, dummy_requests):
        self.base_url = base_url
        self.dummy_requests = dummy_requests
        self.n = len(dummy_requests)
        self.remaining = self.n

        self.dummy_user_credentials = {
            'username': 'sushant',
            'password': 'test123',
            'callback': 'http://127.0.0.1:5000/dummy_callback'
        }
        self.dummy_auth = requests.auth.HTTPBasicAuth(self.dummy_user_credentials['username'],
            self.dummy_user_credentials['password'])
        self.dummy_token_auth = lambda token: requests.auth.HTTPBasicAuth(token, 'unused')

    def pop(self):
        poppedRequest = self.dummy_requests.pop(0)
        self.remaining -= 1

    def top(self):
        return self.dummy_requests[0]

    def is_empty(self):
        return len(self.dummy_requests) == 0

    def execute_all(self):
        #Create a user
        r = requests.post(BASE_URL + '/api/users',
            data = json.dumps(self.dummy_user_credentials),
            headers = JSON_POST_HEADERS)

        has_valid_auth_token = False

        while not self.is_empty():
            # Get auth token
            r = requests.get(BASE_URL + '/api/token',
                headers = {'Accept': "application/json"},
                auth=self.dummy_auth)

            has_valid_auth_token = not is_unauthorised_call(r)
            if not has_valid_auth_token:
                raise Exception('Unauthorised call')

            print "Get new auth token"
            auth_token = r.json()['token']

            # Make requests until token gets expired
            while has_valid_auth_token and not self.is_empty():
                dummy_request = self.top()
                r = call_dummy_request(dummy_request, self.dummy_token_auth(auth_token))
                rNumber = self.n - self.remaining
                if not is_unauthorised_call(r):
                    if is_ok_response(r):
                        print '#' + str(rNumber), r.json()
                        self.pop()
                    else:
                        raise Exception('Dummy request failed: #' + str(rNumber))
                else:
                    has_valid_auth_token = False

DUMMY_REQUESTS = [
    {
      'method': 'POST',
      'type': 'files',
      'url': BASE_URL + '/upload',
      'files': {'file': open('testdata/1.pdf', 'rb')},
      'data': {
          'priority': '0',
          'output-formats': 'txt;html'
      },
      'headers': {'Accept': "application/json"}
    },
    {
        'method': 'POST',
        'type': 'files',
        'url': BASE_URL + '/upload',
        'files': {'file': open('testdata/1.txt', 'rb')},
        'data': {
            'priority': '0',
            'output-formats': 'html;pdf'
        },
        'headers': {'Accept': "application/json"}
    },
    {
        'method': 'POST',
        'type': 'data',
        'url': BASE_URL + '/upload',
        'data': {
            'fileURL': 'http://orgmode.org/worg/org-tutorials/org-publish-html-tutorial.html',
            'priority': '2',
            'output-formats': 'txt;pdf'
        },
        'headers': {'Accept': "application/json"}
    },
    {
        'method': 'POST',
        'type': 'data',
        'url': BASE_URL + '/upload',
        'data': {
            'fileURL': 'http://www.uwgb.edu/nursing/files/docs/Sample-APA-template.doc',
            'priority': '2',
            'output-formats': 'pdf;txt;html'
        },
        'headers': {'Accept': "application/json"}
    },
    {
        'method': 'POST',
        'type': 'files',
        'url': BASE_URL + '/upload',
        'files': {'file': open('testdata/6.pdf', 'rb')},
        'data': {
            'priority': '0',
            'output-formats': 'txt;html'
        },
        'headers': {'Accept': "application/json"}
    },
    {
      'method': 'POST',
      'type': 'data',
      'url': BASE_URL + '/upload',
      'data': {
          'fileURL': 'http://www.snee.com/xml/xslt/sample.doc',
          'priority': '2',
          'output-formats': 'pdf;txt;html'
      },
      'headers': {'Accept': "application/json"}
    },
    {
      'method': 'POST',
      'type': 'files',
      'url': BASE_URL + '/upload',
      'files': {'file': open('testdata/3.pdf', 'rb')},
      'data': {
          'priority': '0',
          'output-formats': 'html;'
      },
      'headers': {'Accept': "application/json"}
    },
    {
      'method': 'POST',
      'type': 'data',
      'url': BASE_URL + '/upload',
      'data': {
          'fileURL': 'http://www.ancestralauthor.com/download/sample.pdf',
          'priority': '2',
          'output-formats': 'html;txt;'
      },
      'headers': {'Accept': "application/json"}
    },
    {
      'method': 'POST',
      'type': 'data',
      'url': BASE_URL + '/upload',
      'data': {
          'fileURL': 'http://www.manning.com/lowagie/sample-ch03_Lowagie.pdf',
          'priority': '2',
          'output-formats': 'txt;html'
      },
      'headers': {'Accept': "application/json"}
    },
]

def dummy_requests_callback():
    print bucket.list()
    pass

def output(result):
    pass

@semisync(callback = output)
def construct_boiler_db():
    # Create all tables and more.
    db.create_all()
    return (True, )

@semisync(callback = output, dependencies = [construct_boiler_db, ])
def test():
    print "Beginning test in 8 seconds"
    time.sleep(8)
    print "Test started..."
    dr = DummyRequests(BASE_URL, DUMMY_REQUESTS)
    dr.execute_all()

    return (True, )

@semisync(callback = output, dependencies = [construct_boiler_db, ])
def run_app():
    mainScript = Command('python app.py')
    mainScript.run(timeout = 3600)
    print "Done with Main script..."
    return (True, )

if __name__ == "__main__":
    construct_boiler_db()
    run_app()
    test()
    semisync.begin()