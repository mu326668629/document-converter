import sys
sys.path.append('..')

from general import GeneralConverter
from xhtml2pdf import pisa
from file_manager import FileManager
from bs4 import BeautifulSoup
import io

class HtmlPdf(GeneralConverter):
    """
    This class is for Html-Pdf conversion.
    """
    def __init__(self, input_file_paths=[]):
        self.initial_format = 'html'
        self.final_format = 'pdf'
        self.file_batch = input_file_paths
        
    def _single_convert(self, input_file_path):
        filemanager = FileManager(input_file_path)
        final_format = self.final_format
        input_file = filemanager.input_file_exists()
        if input_file:
            bytestream = filemanager.get_stream()
            soup = BeautifulSoup(bytestream)
            bytestream = unicode(soup)
            output_file_name = filemanager._get_resultant_file_name(
                final_format)
            output_file = io.open(output_file_name, 'w+b')
            pisa.CreatePDF(bytestream, dest=output_file)
            return output_file_name
