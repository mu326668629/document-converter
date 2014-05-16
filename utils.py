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

FILE_EXTENSIONS = ['pdf', 'txt', 'html', 'doc',
                   'docx', 'ppt', 'pptx', 'rtf', 'odt']

FILE_NAME_LIMIT = 79


class FileAccessDenied(Exception):

    def __init__(self, *args, **kwargs):
        super(FileAccessDenied, self).__init__()
        self.__dict__.update(kwargs)


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
    return re.sub(r'(\.(' + '|'.join(FILE_EXTENSIONS) + '))?$',
                  extension, filename)


def get_filename_from_url(url):
    file_name = url.split('?')[0].split('/')[-1]
    return file_name[-FILE_NAME_LIMIT:]


def download_url(url, destination_dir, target_filename=None, timestamp=True):
    if not target_filename:
        target_filename = get_filename_from_url(url)

    if timestamp:
        target_filename = timestamp_filename(target_filename)

    cdn_response = requests.get(url, stream=True)

    if cdn_response.status_code not 200:
        raise FileAccessDenied(status_code=cdn_response.status_code,
                               message=cdn_response.content)

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


def gzip_file(in_file, unlink=False):
    in_data = open(in_file, "rb").read()
    out_gz = in_file + '.gz'
    gzf = gzip.open(out_gz, "wb")
    gzf.write(in_data)
    gzf.close()

    if unlink:
        os.remove(in_file)
    return out_gz


class ConverterCommand(threading.Thread):

    def __init__(self, cmd, timeout, store_output=None):
        threading.Thread.__init__(self)
        self._cmd = cmd
        self._timeout = timeout
        self._store_output = store_output
        self.return_code = None
        self.output = None

    def run(self):
        if self._store_output:
            log.debug('Command using PIPE')
            self.p = subprocess.Popen(self._cmd, stdout=subprocess.PIPE)
            self.output = self.p.communicate()[0]
            self.return_code = self.p.returncode
        else:
            log.debug('Command not using PIPE')
            self.p = subprocess.Popen(self._cmd)
            self.return_code = self.p.wait()

    def execute(self):
        self.start()
        self.join(self._timeout)

        if self.is_alive():
            self.p.terminate()
            self.join()
