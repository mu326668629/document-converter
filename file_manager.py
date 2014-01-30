import os
import mimetypes
import magic
import re
import io


MIME_TO_EXTENSION = {'text/html': 'html',
                     'application/pdf': 'pdf',
                     'text/plain': 'txt', 
                     'application/msword': 'doc',
                     }

class FileManager:
    def __init__(self, input_file_path, output_file_dir = '', converted = False, output_file_path = None):
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

    def get_output_file_path(self):
        return self.output_file_path

    def set_output_file_path(self, output_extension):
        file_name = os.path.basename(self.input_file_path)
        splitext_output = os.path.splitext(file_name)
        output_file_name = os.path.join(self.output_file_dir, splitext_output[0])
        return '.'.join([output_file_name, output_extension])
