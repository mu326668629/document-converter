import sys
sys.path.append('converters/')

from general import GeneralConverter
from utilities import class_selector
from utils import get_extension

def convert(input_files_objects, output_formats):
    sample_input_file = input_files_objects[0].input_file_path
    input_format = get_extension(sample_input_file)
    converters = [class_selector(input_format, output_format)
                  for output_format in output_formats]
    result = []
    for converter_list in converters:
        for converter, expression in converter_list:
            obj = converter(input_files_objects)
            input_files_objects = obj.convert()
            result.append(obj.convert())
    return result
