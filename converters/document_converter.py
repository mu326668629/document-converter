import sys
sys.path.append('converters/')

from general import GeneralConverter
from utilities import get_input_format, class_selector


def convert(input_files_objects, output_formats):
    input_format = get_input_format(input_files_objects)
    converters = [class_selector(input_format, output_format)
                  for output_format in output_formats]
    result = []
    for converter_list in converters:
        for converter, expression in converter_list:
            print converter
            obj = converter(input_files_objects)
            input_files_objects = obj.convert()
            result.append(obj.convert())
    return result
