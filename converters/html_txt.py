import sys
sys.path.append('..')

from general import GeneralConverter
import html2text
from file_manager import FileManager
from bs4 import BeautifulSoup
import re

class HtmlTxt(GeneralConverter):
    """
    This class is for Html-Text conversion
    """
    def __init__(self, input_file_paths=[]):
        self.initial_format = 'html'
        self.final_format = 'txt'
        self.file_batch = input_file_paths

    def _single_convert(self, input_file_object):
        final_format = self.final_format
        if input_file_object.get_input_file_object():
            h = html2text.HTML2Text()
            h.ignore_links = True
            h.ignore_images = True
            output_extension = final_format
            bytestream = input_file_object.get_stream()
            soup = BeautifulSoup(bytestream)
            [s.extract() for s in soup('script')]
            bytestream = unicode(soup)
            outputstream = h.handle(bytestream)
            output_file = input_file_object.write(output_extension, outputstream)
            if output_file:
                input_file_object.converted = True
                return input_file_object
