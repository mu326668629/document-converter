import sys
import os

sys.path.insert(0, '..')

from config import UPLOAD_FOLDER
PARENT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
TMP_DIR = os.path.join(PARENT_DIR, UPLOAD_FOLDER)
CONVERTER_LOCATION = 'libreoffice --headless --convert-to pdf --outdir {}'.format(TMP_DIR)


from general import GeneralConverter
from utils import rename_filename_with_extension



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
            input_file_path = os.path.join(
                PARENT_DIR,
                input_file_object.get_input_file_path())
            output_file_name = rename_filename_with_extension(
                os.path.basename(input_file_path), 'pdf')
            os.system('%s %s'%(CONVERTER_LOCATION, input_file_path))
            output_file_name = os.path.join(TMP_DIR, output_file_name)
            return output_file_name
        else:
            return None
