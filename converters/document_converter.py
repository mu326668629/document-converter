import sys
sys.path.append('converters/')
sys.path.append('..')

from utilities import class_selector
from file_manager import FileManager
from utils import get_file_extension
from utilities import remove_duplicates

def convert(input_files_objects, output_formats):
    sample_input_file = input_files_objects[0].get_input_file_path()
    input_format = get_file_extension(sample_input_file)
    converters_list = [class_selector(input_format, output_format)
                  for output_format in output_formats]
    converters_list = remove_duplicates(converters_list)
    interim_files_objects = input_files_objects
    for converter, expression in converters_list:
        obj = converter(interim_files_objects)
        interim_files_objects = obj.convert()
        output_files_objects = [FileManager(interim_file_object.get_output_file_path())
                                for interim_file_object in interim_files_objects if interim_file_object]
        interim_files_objects = output_files_objects
    for input_file_object, interim_file_object in zip(input_files_objects, interim_files_objects):
        input_file_object.converted = True
        input_file_object.output_file_path = interim_file_object.get_input_file_path()
    return input_files_objects
