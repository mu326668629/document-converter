import time
import sys
import os
import codecs

sys.path.insert(0, '..')

from logger import log

CONVERTER_LOCATION = '''xvfb-run  /usr/bin/wkhtmltopdf \
--disable-javascript {input_file_path} {output_file_path}'''

from general import GeneralConverter
from utils import (rename_filename_with_extension,
                   remove_tags, log_execution_time)


class HtmlPdf(GeneralConverter):
    """
    This class is for Html-Pdf conversion.
    """

    def __init__(self, input_file_objects=[]):
        super(HtmlPdf, self).__init__(initial_format='html',
                                      final_format='pdf',
                                      input_file_objects=input_file_objects)

    @log_execution_time('html_to_pdf')
    def _single_convert(self, input_file_object):
        if input_file_object:
            input_file_path = input_file_object.get_input_file_path()
            output_file_name = rename_filename_with_extension(
                os.path.basename(input_file_path), self.final_format)

            intermediate_filename = str(time.time()).replace('.', '') + '.html'
            output_file_path = os.path.join(self.tmp_dir, output_file_name)
            intermediate_path = os.path.join(
                self.tmp_dir, intermediate_filename)

            with codecs.open(input_file_path, "r", "utf-8") as f:
                cleaned_content = remove_tags(f.read())
                with open(intermediate_path, 'w') as w:
                    w.write(cleaned_content)

            converter = CONVERTER_LOCATION.format(
                input_file_path=intermediate_path,
                output_file_path=output_file_path)

            self.execute(converter)
            if os.path.isfile(output_file_path):
                return output_file_path
            else:
                self.handle_failed_conversion(input_file_object)

        log.error('Conversion failed from HTML => PDF')
        return None
