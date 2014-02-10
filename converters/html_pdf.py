import sys
sys.path.insert(0, '..')

from general import GeneralConverter
from xhtml2pdf import pisa
from file_manager import FileManager
from utils import rename_filename_with_extension
from bs4 import BeautifulSoup
from config import UPLOAD_FOLDER
import os
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
        input_stream = input_file_object.get_input_stream()
        soup = BeautifulSoup(input_stream)
        invalidAttrs = 'href src width height target style color face size script'.split()
        for attr in invalidAttrs:
            [s.extract() for s in soup(attr)]
        input_stream = unicode(soup)
        output_file_name = rename_filename_with_extension(
            os.path.basename(input_file_object.get_input_file_path()),
            self.final_format)
        output_file = io.open(output_file_name, 'w+b')
        try:
            pisa.CreatePDF(bytestream, dest=output_file)
        except:
            print "Conversion Unsuccessfull for html_pdf"
            return None
        os.system('mv %s %s'%(output_file_name, UPLOAD_FOLDER))
        return os.path.join(UPLOAD_FOLDER, output_file_name)
