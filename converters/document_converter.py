import sys

sys.path.append('..')

from flask_mail import Message

from utilities import class_selector
from utilities import get_input_format
from utilities import set_flags_of_file_objects
from utilities import get_files_objects
from config import ADMINSTRATORS
from config import mail


def convert(input_files_objects, output_format):
    pdf_files_objects = convert_to_pdf(input_files_objects)
    output_files_objects = convert_files(pdf_files_objects, output_format)
    set_flags_of_file_objects(input_files_objects, output_files_objects)
    return input_files_objects


def convert_to_pdf(input_files_objects):
    file_objects = convert_files(input_files_objects, 'pdf')
    return file_objects


def convert_files(input_files_objects, output_format):
    input_format = get_input_format(input_files_objects)
    converters_list = class_selector(input_format, output_format)
    if not converters_list:
        return input_files_objects
    intermediate_files_objects = input_files_objects
    for converter, expression in converters_list:
        converter_object = converter(intermediate_files_objects)
        intermediate_files_paths = converter_object.convert()
        # Temporary fix, please remove this when logic is fexed.
        # remove_input_files(intermediate_files_objects)
        intermediate_files_objects = []
        intermediate_files_objects = get_files_objects(intermediate_files_paths)
    return intermediate_files_objects


def remove_input_files(intermediate_files_objects):
    for intermediate_file_object in intermediate_files_objects:
        if intermediate_file_object:
            intermediate_file_object.remove_input_file()
