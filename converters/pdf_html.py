import os
import sys
sys.path.append('..')

from logger import log
from general import GeneralConverter
from utils import rename_filename_with_extension
from config import UPLOAD_FOLDER

CONVERTER_LOCATION = '''pdf2htmlEX --fit-width 780 --process-outline=0 \
{input_file_path} {output_file_path}'''


class PdfHtml(GeneralConverter):
    """
    This class is for Pdf-Html conversion.
    """
    def __init__(self, input_file_objects=[]):
        super(PdfHtml, self).__init__(initial_format='pdf',
                                      final_format='html',
                                      input_file_objects=input_file_objects)

    def _single_convert(self, input_file_object):
        if input_file_object:
            input_file = input_file_object.get_input_file_path()
            output_file_name = rename_filename_with_extension(
                os.path.basename(input_file), self.final_format)
            output_file_path = os.path.join(self.tmp_dir, output_file_name)

            converter = CONVERTER_LOCATION.format(
                input_file_path=input_file, output_file_path=output_file_path)

            self.execute(converter)

            if os.path.isfile(output_file_path):
                return output_file_path
            else:
                self.handle_failed_conversion(input_file_object)

        log.error('Conversion failed from PDF => HTML')
        return None
