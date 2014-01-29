import sys
sys.path.insert(0, '..')

from general import GeneralConverter
from xhtml2pdf import pisa
from file_manager import FileManager
from bs4 import BeautifulSoup
import io

class HtmlPdf(GeneralConverter):
    """
    This class is for Html-Pdf conversion.
    """
    def __init__(self, file_objects=[]):
        self.initial_format = 'html'
        self.final_format = 'pdf'
        self.file_batch = file_objects
        
    def _single_convert(self, input_file_object):
        final_format = self.final_format
        if input_file_object.get_input_file_object():
            bytestream = input_file_object.get_stream()
            soup = BeautifulSoup(bytestream)
            [s.extract() for s in soup('script')]
            bytestream = unicode(soup)
            output_file_name = input_file_object._get_resultant_file_name(final_format)
            output_file = io.open(output_file_name, 'w+b')
            pisa.CreatePDF(bytestream, dest=output_file)
            if output_file_name:
                input_file_object.converted = True
                return input_file_object
