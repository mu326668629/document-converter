import sys
sys.path.append('..')

from general import GeneralConverter
from file_manager import FileManager
from file_manager import rename_filename_with_extension
from config import UPLOAD_FOLDER
from subprocess import call
import urlparse
import os
import shutil

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
                #TODO: Log the errors
                return None
        else:
            return None
