import sys
sys.path.append('..')

from general import GeneralConverter
import html2text
from file_manager import FileManager
from bs4 import BeautifulSoup
from utils import rename_filename_with_extension
from config import UPLOAD_FOLDER
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
        if input_file_object:
            h = html2text.HTML2Text()
            h.ignore_links = h.ignore_images = True
            input_stream = input_file_object.get_input_stream().encode('utf-8')
            soup = BeautifulSoup(input_stream)
            invalidAttrs = 'href src width height target style color face size script'.split()
            for attr in invalidAttrs:
                [s.extract() for s in soup(attr)]
            input_stream = unicode(soup)
            try:
                output_stream = h.handle(input_stream)
            except:
                print "Conversion Unsuccessfull for html_txt"
                return None
            output_file_name = rename_filename_with_extension(
                os.path.basename(input_file_object.get_input_file_path()),
                self.final_format)
            output_file = write_stream(output_file_name, output_stream)
            try:
                open(output_file)
                os.system('mv %s %s'%(output_file_name, UPLOAD_FOLDER))
                return os.path.join(UPLOAD_FOLDER, output_file_name)
            except IOError:
                print "Conversion Unsuccessfull for html_txt"
                return None
        else:
            return None
