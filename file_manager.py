import os
import io
from config import app
from boto.s3.connection import S3Connection
from boto.s3.key import Key

from utils import download_url, rename_filename_with_extension, gzip_file

AWS_S3_CONNECTION = S3Connection()
AWS_S3_BUCKET = AWS_S3_CONNECTION.get_bucket(app.config['S3_BUCKET'])

def get_signed_url(destination, bucket = AWS_S3_BUCKET):
    bucket_key = Key(bucket)
    bucket_key.key = destination
    return bucket_key.generate_url(3600, query_auth=True, force_http=True)

def upload_to_remote(destination, filepath, bucket = AWS_S3_BUCKET):
    bucket_key = Key(bucket)
    bucket_key.key = destination
    bucket_key.set_contents_from_filename(filepath)
    return destination

def write_stream(destination, stream):
    with io.open(destination, 'w+', encoding='utf-8') as f:
        f.write(stream)
        return destination

class FileManager(object):
    def __init__(self, resource_path, input_file_path = None, **kwargs):
        self.resource_path = resource_path
        self.bucket = kwargs.get('bucket', AWS_S3_BUCKET)
        self.bucket_key = Key(self.bucket)
        
        self.input_file_path = input_file_path
        self.output_file_path = None
        self.remote_destination = None
        self.converted = False

    def is_converted(self):
        return self.converted == True
    
    def get_input_file_path(self):
        if not self.input_file_path:
            remote_path = get_signed_url(self.resource_path, self.bucket)
            self.input_file_path = download_url(remote_path, app.config['UPLOAD_FOLDER'],
                target_filename = os.path.basename(self.resource_path), timestamp = True)
        return self.input_file_path

    def get_input_stream(self):
        return io.open(self.get_input_file_path(), encoding='utf-8').read()

    def remove_input_file(self):
        os.remove(self.input_file_path)

    def get_output_file_path(self):
        return self.output_file_path

    def set_output_file_path(self, filepath):
        self.output_file_path = filepath
        return self.output_file_path

    def remove_output_file(self):
        os.remove(self.output_file_path)

    def set_remote_destination(self, remote_destination):
        self.remote_destination = remote_destination

    def upload_output_file(self):
        self.output_file_path = gzip_file(self.output_file_path, unlink = True)
        if self.remote_destination:
            self.bucket_key.key = self.remote_destination
            self.bucket_key.set_contents_from_filename(self.output_file_path,
                headers = {'Content-Encoding': 'gzip'})
            return get_signed_url(self.remote_destination, self.bucket)
        else:
            raise Exception("REMOTE DESTINATION not provided")
