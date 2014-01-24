import sys
sys.path.append('..')

from general import GeneralConverter
from file_manager import FileManager
from subprocess import call
import urlparse
import os

class PdfHtml(GeneralConverter):
    """
    This class is for Pdf-Html conversion.
    """
    def __init__(self, input_file_paths=[]):
        self.initial_format = 'pdf'
        self.final_format = 'html'
        self.file_batch = input_file_paths

    def _single_convert(self, input_file):
        filemanager = FileManager(input_file)
        input_file = filemanager.input_file_path
        if input_file:
            os.system('pdf2htmlEX %s'%input_file)
            output_file_name = filemanager._get_resultant_file_name(
self.final_format)
            return output_file_name

