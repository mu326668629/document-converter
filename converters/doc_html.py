import sys
sys.path.append('..')
CONVERTER_LOCATION = '/Applications/LibreOffice.app/Contents/MacOS/soffice --headless --convert-to html'
from general import GeneralConverter
from html2text import html2text
from file_manager import FileManager
from bs4 import BeautifulSoup
import re

class DocHtml(GeneralConverter):
    """
    This class is for Doc-Text conversion
    """
    def __init__(self, input_file_paths=[]):
        self.initial_format = 'doc'
        self.final_format = 'html'
        self.file_batch = input_file_paths

    def _single_convert(self, input_file_object):
        input_file_path = input_file_object.input_file_path
        target_output_file = input_file_object.set_output_file_path('html')
        target_output_dir = os.path.dirname(target_output_file)
        output_file_name = os.path.basename(target_output_file)
        os.system('%s %s'%(CONVERTER_LOCATION, input_file_path))
        os.system('mv %s %s'%(output_file_name, target_output_dir))
        if target_output_file:
            input_file_object.output_file_path = target_output_file
            input_file_object.output_file_path = target_output_file
            return input_file_object
