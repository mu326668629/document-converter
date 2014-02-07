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
        bytestream = input_file_object.get_input_stream()
        soup = BeautifulSoup(bytestream)
        invalidAttrs = 'href src width height target style color face size script'.split()
        for attr in invalidAttrs:
            [s.extract() for s in soup(attr)]
        bytestream = unicode(soup)
        output_file_name = rename_filename_with_extension(
            os.path.basename(input_file_object.get_input_file_path()),
            final_format)
        output_file = io.open(output_file_name, 'w+b')
        try:
            pisa.CreatePDF(bytestream, dest=output_file)
        except:
            return None
        if output_file_name:
            return input_file_object
