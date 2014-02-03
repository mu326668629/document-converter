import os
import mimetypes
import magic
import re
import io
from config import app
from boto.s3.connection import S3Connection
from boto.s3.key import Key

AWS_S3_CONNECTION = S3Connection()

bucket = AWS_S3_CONNECTION.get_bucket(app.config['S3_BUCKET'])
bucket_key = Key(bucket)

def get_signed_url(destination):
    bucket_key.key = destination
    return bucket_key.generate_url(3600, query_auth=True, force_http=True)

class FileManager:
    def __init__(self, input_file_path, output_file_dir = '', converted = False,
                output_file_path = None, remote_destination = None):
        self.input_file_path = input_file_path
        if not output_file_dir:
            self.output_file_dir = os.path.dirname(
                os.path.realpath(input_file_path))
        elif output_file_dir == '.':
            self.output_file_dir = ''
        else:
            self.output_file_dir = output_file_dir
        self.output_file_path = output_file_path
        self.converted = converted
        self.remote_destination = remote_destination

    def is_converted(self):
        return self.converted == True
        
    def get_input_file_object(self):
        input_file_path = self.input_file_path
        try:
            file_object = io.open(input_file_path)
        except IOError:
            file_object = None
        return file_object

    def get_stream(self):
        if self.get_input_file_object:
            return io.open(self.input_file_path).read()

    def write(self, output_extension, stream):
        output_file_name = self.set_output_file_path(output_extension)
        with io.open(output_file_name, 'w+') as f:
            f.write(stream)
            return output_file_name

    def get_input_file_path(self):
        return self.input_file_path

    def get_output_file_path(self):
        return self.output_file_path

    def set_output_file_path(self, output_extension):
        file_name = os.path.basename(self.input_file_path)
        splitext_output = os.path.splitext(file_name)
        output_file_name = os.path.join(self.output_file_dir, splitext_output[0])
        return '.'.join([output_file_name, output_extension])

    def set_remote_destination(self, remote_destination):
        self.remote_destination = remote_destination

    def upload_output_file(self):
        if self.remote_destination:
            bucket_key.key = self.remote_destination
            bucket_key.set_contents_from_filename(self.output_file_path)
            return get_signed_url(self.remote_destination)
        else:
            raise Exception("REMOTE DESTINATION not provided")
