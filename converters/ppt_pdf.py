import sys
import os

sys.path.append('..')

from logger import log
from config import UPLOAD_FOLDER, LIBRE_OFFICE_HOST, LIBRE_OFFICE_PORT
PARENT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
TMP_DIR = os.path.join(PARENT_DIR, UPLOAD_FOLDER)
CONVERTER_LOCATION = '''unoconv --connection socket,host={libre_office_host},\
port={libre_office_port},tcpNoDelay=1;urp;StarOffice.ComponentContext -f pdf\
 -o {output_file_path} {input_file_path}'''


from general import GeneralConverter
from utils import rename_filename_with_extension
from utilities import ConverterCommand


class PptPdf(GeneralConverter):
    """
    This class is for ppt-pdf conversion
    """
    def __init__(self, input_file_paths=[]):
        self.initial_format = 'ppt'
        self.final_format = 'pdf'
        self.file_batch = input_file_paths

    def _single_convert(self, input_file_object):
        if input_file_object:
            input_file_path = input_file_object.get_input_file_path()
            output_file_name = rename_filename_with_extension(
                os.path.basename(input_file_path), 'pdf')
            output_file_path = TMP_DIR
            converter = CONVERTER_LOCATION.format(
                libre_office_host=LIBRE_OFFICE_HOST,
                libre_office_port=LIBRE_OFFICE_PORT,
                output_file_path=output_file_path,
                input_file_path=input_file_path)

            command = ConverterCommand(converter.split(), 20)
            command.execute()
            output_file = os.path.join(output_file_path, output_file_name)
            if os.path.isfile(output_file):
                return output_file
            else:
                from .utilities import handle_failed_conversion
                handle_failed_conversion(input_file_path)
                log.error('Conversion failed from PPT => PDF for {}'.format(
                    converter))
        return None
