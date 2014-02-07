import os
import io
from config import app
from boto.s3.connection import S3Connection
from boto.s3.key import Key

from utils import download_url, rename_filename_with_extension

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
    with io.open(destination, 'w+') as f:
        f.write(stream)
        return destination

class FileManager(object):
    def __init__(self, resource_path, **kwargs):
        self.resource_path = resource_path
        self.bucket = kwargs.get('bucket', AWS_S3_BUCKET)
        self.bucket_key = Key(self.bucket)
        
        self.input_file_path = None
        self.output_file_path = None
        self.remote_destination = None
        self.converted = False

    def is_converted(self):
        return self.converted == True
    
    def get_input_file(self):
        remote_path = get_signed_url(self.resource_path, self.bucket)
        self.input_file_path = download_url(remote_path,
            app.config['UPLOAD_FOLDER'])
        return self.input_file_path

    def get_input_stream(self):
        if not self.input_file_path:
            self.input_file_path = self.get_input_file()
        return io.open(self.input_file_path).read()

    def get_input_file_path(self):
        return self.input_file_path

    def remove_input_file(self):
        os.remove(self.input_file_path)

    def write_output_file(self, output_extension, stream):
        if not self.output_file_path:
            self.set_output_file_path(output_extension)

        with io.open(self.output_file_path, 'w+') as f:
            f.write(stream)
            return self.output_file_path

    def get_output_file_path(self):
        return self.output_file_path

    def set_output_file_path(self, output_extension):
        filename = rename_filename_with_extension(
            os.path.basename(self.input_file_path), output_extension)

        self.output_file_path = os.path.join(
            app.config['OUTPUT_FOLDER'], filename)

        return self.output_file_path

    def remove_output_file(self):
        os.remove(self.output_file_path)

    def set_remote_destination(self, remote_destination):
        self.remote_destination = remote_destination

    def upload_output_file(self):
        if self.remote_destination:
            self.bucket_key.key = self.remote_destination
            self.bucket_key.set_contents_from_filename(self.output_file_path)
            return get_signed_url(self.remote_destination, self.bucket)
        else:
            raise Exception("REMOTE DESTINATION not provided")