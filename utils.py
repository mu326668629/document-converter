import re
import os
import time
import magic
import mimetypes
import subprocess
import threading
import requests

MIME_TO_EXTENSION = {
    'text/html': 'html',
    'application/pdf': 'pdf',
    'text/plain': 'txt', 
    'application/msword': 'doc',
}

def get_attrs(klass):
    return [k for k in klass.__dict__.keys()
        if not k.startswith('__')
        and not k.endswith('__')]

def timestamp_filename(filename):
    return str(int(time.time()*1000)) + '_' + filename

def allowed_filename(filename, possible_extensions):
    extensionRegExp = '|'.join(possible_extensions)
    return bool(re.match(r'.*\.(' + extensionRegExp + ')$', filename))

def get_filename_from_url(url):
    return url.split('/')[-1]

def download_url(url, destination_dir, timestamp = True):
    local_filename = get_filename_from_url(url)
    if timestamp:
        local_filename = timestamp_filename(local_filename)

    r = requests.get(url, stream=True)
    local_filepath = os.path.join(destination_dir, local_filename)

    with open(local_filepath, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
                
    return local_filename

def get_extension(file_path):
    mime_type = get_mime_type(file_path)
    extension = MIME_TO_EXTENSION.get(mime_type)
    if not extension:
        expression = re.compile('\.\w+$')
        extensions = expression.findall(file_path)
        if extensions:
            extension = extensions[0][1:]
    return extension

def get_mime_type(file_path):
    try:
        mime_type = magic.from_file(
            file_path.encode('utf-8'), mime=True)
    except IOError, e:
        print e
        mime_type = None
    if mime_type is None:
        mime_type, mime_encoding = mimetypes.guess_type(
            file_path.encode('utf-8'), strict=True)
        # accepts unicode as well. For consistency using utf
    return mime_type

class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None

    def run(self, timeout):
        def target():
            print 'Thread started'
            self.process = subprocess.Popen(self.cmd, shell=True)
            self.process.communicate()
            print 'Thread finished'

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            print 'Terminating process'
            self.process.terminate()
            thread.join()
        print self.process.returncode

class PidManager(object):
    def __init__(self, pid_file_path):
        self.pid_file_path = pid_file_path
        if not os.path.isfile(self.pid_file_path):
            self._write('10000000')

    def _write(self, val):
        pid_file = open(self.pid_file_path, 'w')
        pid_file.write(str(val))
        pid_file.close()

    def _read_pid(self):
        pid_file = open(self.pid_file_path, 'r')
        pid = int(pid_file.read().strip())
        pid_file.close()
        return pid

    def register(self):
        self._write(str(os.getpid()))

    def is_running(self):
        pid = self._read_pid()
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False