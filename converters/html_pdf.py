import sys
import os

sys.path.insert(0, '..')

from logger import log

from config import UPLOAD_FOLDER
PARENT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
TMP_DIR = os.path.join(PARENT_DIR, UPLOAD_FOLDER)
CONVERTER_LOCATION = '''xvfb-run\
 /usr/bin/wkhtmltopdf {input_file_path} {output_file_path}'''


from general import GeneralConverter
from utils import rename_filename_with_extension
from converters.utilities import ConverterCommand


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

            output_file_path = os.path.join(TMP_DIR, output_file_name)
            converter = CONVERTER_LOCATION.format(
                input_file_path=input_file_path,
                output_file_path=output_file_path)

            command = ConverterCommand(converter.split(), 20)
            command.execute()
            if os.path.isfile(output_file_path):
                return output_file_path
            else:
                from .utilities import handle_failed_conversion
                handle_failed_conversion(input_file_path)
                log.error('Conversion failed from HTML => PDF for {}'.format(
                    converter))
        return None
