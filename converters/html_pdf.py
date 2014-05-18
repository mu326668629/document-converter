import time
import sys
import os
import subprocess
import codecs

sys.path.insert(0, '..')

from logger import log

from config import UPLOAD_FOLDER
PARENT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
TMP_DIR = os.path.join(PARENT_DIR, UPLOAD_FOLDER)
CONVERTER_LOCATION = '''xvfb-run\
 /usr/bin/wkhtmltopdf --disable-javascript {input_file_path} {output_file_path}'''


from general import GeneralConverter
from utils import rename_filename_with_extension, remove_tags


class HtmlPdf(GeneralConverter):
    """
    This class is for Html-Pdf conversion.
    """
    def __init__(self, input_file_paths=[]):
        self.initial_format = 'html'
        self.final_format = 'pdf'
        self.file_batch = input_file_paths

    def _single_convert(self, input_file_object):
        if input_file_object:
            input_file_path = input_file_object.get_input_file_path()
            output_file_name = rename_filename_with_extension(
                os.path.basename(input_file_path), 'pdf')
            
            intermediate_filename = str(time.time()).replace('.', '') + '.html'
            output_file_path = os.path.join(TMP_DIR, output_file_name)
            intermediate_path = os.path.join(TMP_DIR, intermediate_filename)

            with codecs.open(input_file_path, "r", "utf-8") as f:
                cleaned_content = remove_tags(f.read())
                with open(intermediate_path, 'w') as w:
                    w.write(cleaned_content)

            converter = CONVERTER_LOCATION.format(
                input_file_path=intermediate_path,
                output_file_path=output_file_path)

            subprocess.call(converter.split())
            if os.path.isfile(output_file_path):
                return output_file_path
            else:
                from .utilities import handle_failed_conversion
                handle_failed_conversion(input_file_path)
                log.error('Conversion failed from HTML => PDF for {}'.format(
                    converter))
        return None

{'a':
1,
'sys':
[]
}
