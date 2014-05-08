import sys
import os
import html2text

sys.path.append('..')

from logger import log
from general import GeneralConverter
from bs4 import BeautifulSoup
from utils import rename_filename_with_extension
from file_manager import write_stream

from config import UPLOAD_FOLDER
PARENT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
TMP_DIR = os.path.join(PARENT_DIR, UPLOAD_FOLDER)

class HtmlTxt(GeneralConverter):
    """
    This class is for Html-Text conversion
    """
    def __init__(self, input_file_paths=[]):
        self.initial_format = 'html'
        self.final_format = 'txt'
        self.file_batch = input_file_paths

    def _single_convert(self, input_file_object):
        from .utilities import handle_failed_conversion
        if input_file_object:
            input_file_path = input_file_object.get_input_file_path()
            log.info('Converting {} to TXT'.format(input_file_path))
            h = html2text.HTML2Text()
            h.ignore_links = h.ignore_images = True
            try:
                input_stream = input_file_object.get_input_stream()
            except UnicodeDecodeError, e:
                handle_failed_conversion(input_file_path)
                log.error('Conversion failed from HTML => TXT for {} {}'.format(
                    input_file_path, e))
                return None
            soup = BeautifulSoup(input_stream)
            invalidAttrs = 'href src width height target style color face size script'.split()
            for attr in invalidAttrs:
                [s.extract() for s in soup(attr)]
            input_stream = unicode(soup)
            try:
                output_stream = h.handle(input_stream)
            except e:
                handle_failed_conversion(input_file_path)
                log.error('Conversion failed from HTML => TXT for {} {}'.format(
                    input_file_path, e))
                return None
            output_file_name = rename_filename_with_extension(
                os.path.basename(input_file_object.get_input_file_path()),
                self.final_format)
            output_file_path = os.path.join(TMP_DIR, output_file_name)
            output_file = write_stream(output_file_path, output_stream)

            if os.path.isfile(output_file_path):
                return output_file_path
            else:
                handle_failed_conversion(input_file_path)
                log.error('Conversion failed from HTML => TXT for {}'.format(
                    input_file_path))

        return None
