import sys
sys.path.insert(0, '..')

from general import GeneralConverter
from file_manager import FileManager
import markdown2
import io

class TxtHtml(GeneralConverter):
    """
    This class is for Txt-Html conversion.
    """
    def __init__(self, input_file_paths=[]):
        self.initial_format = 'txt'
        self.final_format = 'html'
        self.file_batch = input_file_paths

    def _single_convert(self, input_file_object):
        input_stream = input_file_object.get_stream()
        output_stream = markdown2.markdown(input_stream)
        output_file = input_file_object.write(self.final_format, output_stream)
        if output_file:
            return FileManager(output_file)
