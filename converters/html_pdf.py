import sys
sys.path.append('..')

from general import GeneralConverter
from xhtml2pdf import pisa
from file_manager import FileManager

class HtmlPdf(GeneralConverter):
    """
    This class is for Html-Pdf conversion.
    """
    def __init__(self, *file_paths):
        self.initial_format = 'html'
        self.final_format = 'pdf'
        self.file_batch = [file_path for file_path in file_paths]

    def convert(self, input_file_path):
        filemanager = FileManager(input_file_path)
        final_format = self.final_format
        if filemanager.input_file_exists:
            input_file = filemanager.input_file_exists
            text = filemanager.get_stream()
            output_file_name = filemanager._get_resultant_file_name(final_format)
            output_file = open(output_file_name, 'w+b')
            pisa.CreatePDF(text, dest=output_file)
            return output_file_name
