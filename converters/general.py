import os
import sys
sys.path.append('..')

from config import UPLOAD_FOLDER, OUTPUT_FOLDER
from utils import ConverterCommand

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
TMP_DIR = os.path.join(PARENT_DIR, UPLOAD_FOLDER)
OUTPUT_DIR = os.path.join(PARENT_DIR, OUTPUT_FOLDER)


class GeneralConverter(object):

    """
    This is the base class of all converters.
    """

    def __init__(self, initial_format=None, final_format=None,
                 input_file_objects=None):
        """
        The attributes get initlalized in subclasses.
        """
        self.output_dir = OUTPUT_DIR
        self.tmp_dir = TMP_DIR

        self.initial_format = initial_format
        self.final_format = final_format
        self.file_batch = input_file_objects

    def convert(self):
        return [self._single_convert(input_file_object)
                for input_file_object in self.file_batch]

    def execute(self, converter):
        command = ConverterCommand(converter.split(), 20)
        return command.execute()
