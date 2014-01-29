import sys
sys.path.append('..')
sys.path.append('.')

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
        self.file_batch = input_file_objects

    def _single_convert(self, input_file_object):
        input_file = input_file_object.input_file_path
        if input_file:
            output_file_name = input_file_object._get_resultant_file_name(self.final_format)
            output_file_dir = os.path.basename(os.path.dirname(output_file_name))
            temp_output_file = os.path.join(output_file_dir, output_file_name)
            output_file = os.path.join(os.path.basename(os.path.dirname(temp_output_file)), os.path.basename(temp_output_file))
            os.system('pdf2htmlEX %s %s'%(input_file, output_file))
            if output_file_name:
                input_file_object.converted = True
                return input_file_object

