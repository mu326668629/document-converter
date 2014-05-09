import sys
sys.path.append('..')

from logger import log
from general import GeneralConverter
from utils import rename_filename_with_extension
from config import UPLOAD_FOLDER
import os


class PdfHtml(GeneralConverter):
    """
    This class is for Pdf-Html conversion.
    """
    def __init__(self, input_file_objects=[]):
        self.initial_format = 'pdf'
        self.final_format = 'html'
        self.file_batch = input_file_objects

    def _single_convert(self, input_file_object):
        if input_file_object:
            input_file = input_file_object.get_input_file_path()
            output_file_name = rename_filename_with_extension(
                os.path.basename(input_file), 'html')
            os.system('pdf2htmlEX --fit-width 780 --process-outline=0 %s'%input_file)
            try:
                open(output_file_name)
                os.system('mv %s %s'%(output_file_name, UPLOAD_FOLDER))
                return os.path.join(UPLOAD_FOLDER, output_file_name)
            except IOError:
                from .utilities import handle_failed_conversion
                input_file_path = input_file_object.get_input_file_path()
                handle_failed_conversion(input_file_path)
                log.error('Conversion failed from PDF => HTML for {}'.format(
                    input_file_path))
                return None
        else:
            return None
