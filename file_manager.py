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
    def __init__(self, input_file_path, output_file_path = '', converted = False):
        self.input_file_path = input_file_path
        if not output_file_path:
            self.output_file_path = os.path.dirname(
                os.path.realpath(input_file_path))
        else:
            self.output_file_path = output_file_path
        self.converted = converted

    def conversion_status(self):
        return self.converted
        
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
        output_file_name = self._get_resultant_file_name(output_extension)
        with io.open(output_file_name, 'w+') as f:
            f.write(stream)
            return output_file_name

    def _get_resultant_file_name(self, output_extension):
        file_name = os.path.basename(self.input_file_path)
        splitext_output = os.path.splitext(file_name)
        output_file_name = os.path.join(self.output_file_path, splitext_output[0])
        return '.'.join([output_file_name, output_extension])

    def get_extension(self):
        mime_type = self.get_mime_type()
        extension = MIME_TO_EXTENSION.get(mime_type)
        if not extension:
            expression = re.compile('\.\w+$')
            extensions = expression.findall(self.input_file_path)
            if extensions:
                extension = extensions[0][1:]
        return extension

    def get_mime_type(self):
        try:
            mime_type = magic.from_file(
                self.input_file_path.encode('utf-8'), mime=True)
        except IOError, e:
            print e
            mime_type = None
        if mime_type is None:
            mime_type, mime_encoding = mimetypes.guess_type(
                self.input_file_path.encode('utf-8'), strict=True)
            # accepts unicode as well. For consistency using utf
        return mime_type
