import os
import sys
import subprocess
import logging as log
sys.path.append('..')

from config import UPLOAD_FOLDER, LIBRE_OFFICE_HOST, LIBRE_OFFICE_PORT
PARENT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
TMP_DIR = os.path.join(PARENT_DIR, UPLOAD_FOLDER)
CONVERTER_LOCATION = '''nice libreoffice --headless --convert-to pdf:writer_pdf_Export --outdir
 {output_file_path} {input_file_path}'''


from general import GeneralConverter
from file_manager import rename_filename_with_extension


class DocPdf(GeneralConverter):
    """
    This class is for Doc-Pdf conversion
    """
    def __init__(self, input_file_paths=[]):
        self.initial_format = 'doc'
        self.final_format = 'pdf'
        self.file_batch = input_file_paths

    def _single_convert(self, input_file_object):
        if input_file_object:
            input_file_path = input_file_object.get_input_file_path()
            output_file_name = rename_filename_with_extension(
                os.path.basename(input_file_path), 'pdf')

            output_file_path = TMP_DIR
            converter = CONVERTER_LOCATION.format(
                output_file_path=output_file_path,
                input_file_path=input_file_path)

            subprocess.call(converter.split())
            output_file = os.path.join(output_file_path, output_file_name)
            if os.path.isfile(output_file):
                return output_file
            else:
                log.error('Conversion failed from DOC => PDF for {}'.format(
                    input_file_path))
        return None
