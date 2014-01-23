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
    def __init__(self, *file_paths):
        self.initial_format = 'pdf'
        self.final_format = 'html'
        self.file_batch = [file_path for file_path in file_paths]

    def convert(self, f):
        filemanager = FileManager(f)
        input_file = filemanager.input_file_path
        os.system('pdf2htmlEX %s'%input_file)
        output_file_name = filemanager._get_resultant_file_name(self.final_format)
        return output_file_name
