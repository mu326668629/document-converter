import os
import mimetypes
import magic
import io

class FileManager:

    def __init__(self, input_file_path, output_file_path = None):
        self.input_file_path = input_file_path
        if not output_file_path:
            self.output_file_path = os.path.dirname(os.path.realpath(input_file_path))
        else:
            self.output_file_path = output_file_path
        
    def input_file_exists(self):
        input_file_path = self.input_file_path
        try:
            file_object = open(input_file_path)
        except IOError:
            file_object = None
        return file_object

    def get_stream(self):
        if self.input_file_exists:
            return io.open(self.input_file_path).read()

    def write(self, output_extension, stream):
        output_file = self._get_resultant_file_name(output_extension)
        with io.open(output_file, 'w+') as f:
            f.write(stream)
        return output_file

    def _get_resultant_file_name(self, output_extension):
        file_name = os.path.basename(self.input_file_path)
        splitext_output = os.path.splitext(file_name)
        return '.'.join([splitext_output[0], output_extension])

    def get_extension(self, file_path):
        mime_type = get_mime_type(file_path)
        if re.compile('.*plain.*', re.IGNORECASE).match(mime_type) or re.compile('.*pretty.*', re.IGNORECASE).match(mime_type):
            return 'txt'
        elif re.compile('.*html.*', re.IGNORECASE).match(mime_type):
            return 'html'
        elif re.compile('.*pdf.*', re.IGNORECASE).match(mime_type):
            return 'pdf'

    def get_mime_type(self, original_file_path):
        try:
            mime_type = magic.from_file(
            original_file_path.encode('utf-8'), mime=True)
        except IOError, e:
            print e
            mime_type = None
        if mime_type is None:
            mime_type, mime_encoding = mimetypes.guess_type(
                original_file_path.encode('utf-8'), strict=True)
            # accepts unicode as well. For consistency using utf
            return mime_type
