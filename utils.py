import re
import os
import gzip
import uuid
import time
import magic
import mimetypes
import subprocess
import threading
import requests

from logger import log

MIME_TO_EXTENSION = {
    'text/html': 'html',
    'application/pdf': 'pdf',
    'text/plain': 'txt',
    'application/msword': 'doc',
    'application/vnd.oasis.opendocument.text': 'doc',
}

FILE_EXTENSIONS = ['pdf', 'txt', 'html', 'doc', 'docx', 'ppt', 'pptx', 'rtf', 'odt']

def get_attrs(klass):
    return [k for k in klass.__dict__.keys()
        if not k.startswith('__')
        and not k.endswith('__')]

def get_uuid():
    return uuid.uuid4().hex

def timestamp_filename(filename):
    return str(int(time.time()*1000)) + '_' + filename

def allowed_filename(filename, possible_extensions):
    extensionRegExp = '|'.join(possible_extensions)
    return bool(re.match(r'.*\.(' + extensionRegExp + ')$', filename))

def rename_filename_with_extension(filename, extension):
    extension = extension if extension.startswith('.') else '.' + extension
    return re.sub(r'(\.(' + '|'.join(FILE_EXTENSIONS) + '))?$', extension, filename)

def get_filename_from_url(url):
    return url.split('?')[0].split('/')[-1]

def download_url(url, destination_dir, target_filename = None, timestamp = True):
    if not target_filename:
        target_filename = get_filename_from_url(url)

    if timestamp:
        target_filename = timestamp_filename(target_filename)

    r = requests.get(url, stream=True)
    target_filepath = os.path.join(destination_dir, target_filename)

    with open(target_filepath, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()

    return target_filepath

def get_extension_from_filename(filename):
    extensions = re.findall('\.\w+$', filename)
    if extensions:
        return extensions[0][1:]

def get_file_extension(file_path):
    mime_type = get_mime_type(file_path)
    extension = MIME_TO_EXTENSION.get(mime_type)
    if not extension:
        extension = get_extension_from_filename(file_path)
    return extension

def get_mime_type(file_path):
    try:
        mime_type = magic.from_file(
            file_path.encode('utf-8'), mime=True)
    except IOError, e:
        log.error('Error getting MIME type : {}'.format(e))
        mime_type = None
    if mime_type is None:
        mime_type, mime_encoding = mimetypes.guess_type(
            file_path.encode('utf-8'), strict=True)
        # accepts unicode as well. For consistency using utf
    return mime_type

def gzip_file(in_file, unlink = False):
    in_data = open(in_file, "rb").read()
    out_gz = in_file + '.gz'
    gzf = gzip.open(out_gz, "wb")
    gzf.write(in_data)
    gzf.close()

    if unlink:
        os.remove(in_file)
    return out_gz

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

# class PidManager(object):
#     def __init__(self, pid_file_path):
#         self.pid_file_path = pid_file_path
#         if not os.path.isfile(self.pid_file_path):
#             self._write('10000000')

#     def _write(self, val):
#         pid_file = open(self.pid_file_path, 'w')
#         pid_file.write(str(val))
#         pid_file.close()

#     def _read_pid(self):
#         pid_file = open(self.pid_file_path, 'r')
#         pid = int(pid_file.read().strip())
#         pid_file.close()
#         return pid

#     def register(self):
#         self._write(str(os.getpid()))

#     def is_running(self):
#         pid = self._read_pid()
#         try:
#             os.kill(pid, 0)
#             return True
#         except OSError:
#             return False
