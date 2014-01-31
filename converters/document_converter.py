import sys
sys.path.append('converters/')

from general import GeneralConverter
from utilities import class_selector
from utilities import remove_duplicates
from utilities import FileManager
from utils import get_file_extension
from sets import Set

def convert(input_files_objects, output_formats):
    sample_input_file = input_files_objects[0].input_file_path
    input_format = get_file_extension(sample_input_file)
    converters_list = [class_selector(input_format, output_format)
                  for output_format in output_formats]
    converters_list = remove_duplicates(converters_list)
    result = []
    interm_files_objects = input_files_objects
    for converter, expression in converters_list:
        obj = converter(interm_files_objects)
        interm_files_objects = obj.convert()
        output_files_objects = [FileManager(interm_file_object.output_file_path)
                               for interm_file_object in interm_files_objects]
        interm_files_objects = output_files_objects
    for input_file_object, interm_file_object in input_files_objects interm_files_objects:
        input_file_object.converted = True
        input_file_object.output_file_path = interm_files_objects.get_output_file_path()
    return input_files_objects
