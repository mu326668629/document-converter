import sys
sys.path.insert(0, '..')

from general import GeneralConverter
from file_manager import FileManager
from file_manager import write_stream
from utils import rename_filename_with_extension
from config import UPLOAD_FOLDER
import markdown2
import io
import os

class TxtHtml(GeneralConverter):
    """
    This class is for Txt-Html conversion.
    """
    def __init__(self, input_file_paths=[]):
        self.initial_format = 'txt'
        self.final_format = 'html'
        self.file_batch = input_file_paths

    def _single_convert(self, input_file_object):
        if input_file_object:
            input_stream = input_file_object.get_input_stream()
            try:
                output_stream = markdown2.markdown(input_stream)
            except:
                print "Conversion Unsuccessfull for txt_html"
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

        log.error('Conversion failed from TXT => HTML')
        return None
