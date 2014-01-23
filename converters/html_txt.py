import sys
sys.path.append('..')

from general import GeneralConverter
from html2text import html2text
from file_manager import FileManager

class HtmlTxt(GeneralConverter):
    """
    This class is for Html-Text conversion
    """
    def __init__(self, *file_paths):
        self.initial_format = 'html'
        self.final_format = 'txt'
        self.file_batch = [file_path for file_path in file_paths]

    def convert(self, input_file):
        final_format = self.final_format
        filemanager = FileManager(input_file)
        if filemanager.input_file_exists():
            output_extension = final_format
            bytestream = filemanager.get_stream()
            outputstream = html2text(bytestream)
            output_file = filemanager.write(output_extension, outputstream)
            return output_file
