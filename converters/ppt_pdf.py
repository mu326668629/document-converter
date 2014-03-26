import sys
sys.path.append('..')


CONVERTER_LOCATION = 'libreoffice --headless --convert-to pdf'


from general import GeneralConverter
from file_manager import FileManager
from file_manager import rename_filename_with_extension
from config import UPLOAD_FOLDER
import os

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
            os.system('%s %s'%(CONVERTER_LOCATION, input_file_path))
            try:
                open(output_file_name)
                os.system('mv %s %s'%(output_file_name, UPLOAD_FOLDER))
                return os.path.join(UPLOAD_FOLDER, output_file_name)
            except IOError:
                print "Conversion Unsuccessfull for ppt_pdf"
                return None
        else:
            return None
