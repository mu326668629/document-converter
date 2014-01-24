import sys
sys.path.append('..')

from general import GeneralConverter
from html2text import html2text
from file_manager import FileManager
from bs4 import BeautifulSoup

class HtmlTxt(GeneralConverter):
    """
    This class is for Html-Text conversion
    """
    def __init__(self, input_file_paths=[]):
        self.initial_format = 'html'
        self.final_format = 'txt'
        self.file_batch = input_file_paths

    def _single_convert(self, input_file):
        final_format = self.final_format
        filemanager = FileManager(input_file)
        if filemanager.input_file_exists():
            output_extension = final_format
            bytestream = filemanager.get_stream()
            soup = BeautifulSoup(bytestream)
            bytestream = str(soup)
            outputstream = html2text(bytestream)
            output_file = filemanager.write(output_extension, outputstream)
            return output_file
