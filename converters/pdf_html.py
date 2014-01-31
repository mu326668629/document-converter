import sys
sys.path.append('..')
sys.path.append('.')

from general import GeneralConverter
from file_manager import FileManager
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
        input_file = input_file_object.input_file_path
        print input_file
        target_output_file = input_file_object.set_output_file_path('html')
        target_output_dir = os.path.dirname(target_output_file)
        output_file_name = os.path.basename(target_output_file)
        os.system('pdf2htmlEX %s'%input_file)
        os.system('mv %s %s'%(output_file_name, target_output_dir))
        if target_output_file:
            input_file_object.output_file_path = target_output_file
            input_file_object.output_file_path = target_output_file
            return input_file_object
        

        #shutil.move(output_file_name, target_output_dir)
