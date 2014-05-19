import sys
import os

sys.path.append('..')

from logger import log
CONVERTER_LOCATION = '''nice libreoffice --headless --convert-to\
 pdf:writer_pdf_Export --outdir {output_file_path} {input_file_path}'''


from general import GeneralConverter
from utils import rename_filename_with_extension


class PptPdf(GeneralConverter):
    """
    This class is for ppt-pdf conversion
    """
    def __init__(self, input_file_objects=[]):
        super(PptPdf, self).__init__(initial_format='ppt',
                                     final_format='pdf',
                                     input_file_objects=input_file_objects)

    def _single_convert(self, input_file_object):
        if input_file_object:
            input_file_path = input_file_object.get_input_file_path()
            output_file_name = rename_filename_with_extension(
                os.path.basename(input_file_path), self.final_format)

            output_file_path = self.tmp_dir
            converter = CONVERTER_LOCATION.format(
                output_file_path=output_file_path,
                input_file_path=input_file_path)

            self.execute(converter)
            output_file = os.path.join(output_file_path, output_file_name)
            if os.path.isfile(output_file):
                return output_file
            else:
                self.handle_failed_conversion(input_file_object)

        log.error('Conversion failed from PPT => PDF')
        return None
