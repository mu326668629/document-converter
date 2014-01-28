import sys
sys.path.append('..')

from general import GeneralConverter
from html2text import html2text
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
            output_extension = final_format
            bytestream = input_file_object.get_stream()
            soup = BeautifulSoup(bytestream)
            [s.extract() for s in soup('script')]
            [s.extract() for s in soup('style')]
            bytestream = unicode(soup)
            outputstream = html2text(bytestream)
            outputstring = str(outputstream)
            expression = re.compile('!\[\]\(data:image.*\)')
            outputstring = re.sub(expression, '', outputstring)
            outputstream = unicode(outputstring)
            output_file = input_file_object.write(output_extension, outputstream)
            if output_file:
                return FileManager(output_file)
