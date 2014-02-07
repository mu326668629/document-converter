import sys
sys.path.append('..')

from general import GeneralConverter
import html2text
from file_manager import FileManager
from bs4 import BeautifulSoup
from utils import rename_filename_with_extension
from file_manager import write_stream

import re
import os

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
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        output_extension = final_format
        bytestream = input_file_object.get_input_stream()
        soup = BeautifulSoup(bytestream)
        invalidAttrs = 'href src width height target style color face size script'.split()
        for attr in invalidAttrs:
            [s.extract() for s in soup(attr)]
        bytestream = unicode(soup)
        try:
            outputstream = h.handle(bytestream)
        except:
            return None
        output_file_name = rename_filename_with_extension(
            os.path.basename(input_file_object.get_input_file_path()),
            final_format)
        output_file = write_stream(output_file_name, outputstream)
        if output_file:
            return input_file_object
