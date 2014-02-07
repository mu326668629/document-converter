import sys
sys.path.insert(0, '..')

from general import GeneralConverter
from file_manager import FileManager
from file_manager import write_stream
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
        input_stream = input_file_object.get_input_stream()
        try:
            output_stream = markdown2.markdown(input_stream)
        except:
            return None
        output_file_name = rename_filename_with_extension(
            os.path.basename(input_file_object.get_input_file_path()),
            final_format)
        output_file = write_stream(output_file_name, output_stream)
        if output_file:
            return input_file_object
