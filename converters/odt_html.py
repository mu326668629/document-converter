import sys
sys.path.append('..')
CONVERTER_LOCATION = '/Applications/LibreOffice.app/Contents/MacOS/soffice --headless --convert-to txt --outdir'
from general import GeneralConverter
from html2text import html2text
from file_manager import FileManager
from bs4 import BeautifulSoup
import re

class OdtTxt(GeneralConverter):
    """
    This class is for Odt-Text conversion
    """
    def __init__(self, input_file_paths=[]):
        self.initial_format = 'odt'
        self.final_format = 'txt'
        self.file_batch = input_file_paths

    def _single_convert(self, input_file_object):
        input_file_path = input_file_object.input_file_path
        output_file_path = input_file_object.output_file_path
        
        
