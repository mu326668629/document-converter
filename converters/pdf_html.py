import sys
sys.path.insert(0, '..')

from general import GeneralConverter
from file_manager import FileManager
from subprocess import call
import urlparse
import os

class PdfHtml(GeneralConverter):
    """
    This class is for Pdf-Html conversion.
    """
    def __init__(self, input_file_objects=[]):
        self.initial_format = 'pdf'
        self.final_format = 'html'
        self.file_batch = input_file_

    def _single_convert(self, input_file_object):
        input_file = input_file_object.input_file_path
        if input_file:
            output_file_name = input_file_object._get_resultant_file_name(self.final_format)
            os.system('pdf2htmlEX %s %s'%(input_file, output_file_name))
            if output_file_name:
                return FileManager(output_file_name)

