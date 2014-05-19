import sys
import os
import html2text

sys.path.append('..')

from logger import log
from general import GeneralConverter
from bs4 import BeautifulSoup
from utils import rename_filename_with_extension
from file_manager import write_stream


class HtmlTxt(GeneralConverter):
    """
    This class is for Html-Text conversion
    """

    def __init__(self, input_file_objects=[]):
        super(HtmlTxt, self).__init__(initial_format='html',
                                      final_format='txt',
                                      input_file_objects=input_file_objects)

    def _single_convert(self, input_file_object):
        if input_file_object:
            input_file_path = input_file_object.get_input_file_path()
            log.info('Converting {} to TXT'.format(input_file_path))
            html_to_text = html2text.HTML2Text()
            html_to_text.ignore_links = html_to_text.ignore_images = True
            try:
                input_stream = input_file_object.get_input_stream()
            except UnicodeDecodeError, e:
                self.handle_failed_conversion(input_file_object)
                log.error(
                    'Conversion failed from HTML => TXT for {} {}'.format(
                        input_file_path, e)
                )
                return None

            soup = BeautifulSoup(input_stream)
            invalid_attrs = 'href src width height target \
            style color face size script'.split()

            for attr in invalid_attrs:
                [dom_el.extract() for dom_el in soup(attr)]
            input_stream = unicode(soup)

            try:
                output_stream = html_to_text.handle(input_stream)
            except e:
                self.handle_failed_conversion(input_file_object)
                log.error(
                    'Conversion failed from HTML => TXT for {} {}'.format(
                        input_file_path, e)
                )
                return None

            output_file_name = rename_filename_with_extension(
                os.path.basename(input_file_object.get_input_file_path()),
                self.final_format)
            output_file_path = os.path.join(self.tmp_dir, output_file_name)
            write_stream(output_file_path, output_stream)

            if os.path.isfile(output_file_path):
                return output_file_path
            else:
                self.handle_failed_conversion(input_file_object)

        self.handle_failed_conversion(input_file_object)
        log.error('Conversion failed from HTML => TXT')
        return None
