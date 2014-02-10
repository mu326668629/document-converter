import sys
sys.path.append('converters/')
sys.path.append('..')

from utilities import class_selector
from file_manager import FileManager
from utils import get_file_extension
from utilities import remove_duplicates
from config import OUTPUT_FOLDER
import os

def convert(input_files_objects, output_formats):
    sample_input_file = input_files_objects[0].get_input_file_path()
    input_format = get_file_extension(sample_input_file)
    converters = [class_selector(input_format, output_format)
                  for output_format in output_formats]
    converters = remove_duplicates(converters)
    interim_files_objects = input_files_objects
    for converter, expression in converters:
        obj = converter(interim_files_objects)
        interim_files_paths = obj.convert()
        [interim_file_object.remove_input_file() for
         interim_file_object in interim_files_objects]
        interim_files_objects = [FileManager(None, input_file_path = interim_file_path) for 
                                 interim_file_path in interim_files_paths]
    temp_files_paths = [file_object.get_input_file_path() for
                         file_object in interim_files_objects]
    output_files_paths = [os.path.join(OUTPUT_FOLDER, os.path.basename(temp_file_path)) for
                          temp_file_path in temp_files_paths]
    [os.system('mv %s %s'%(file_path, OUTPUT_FOLDER)) for
     file_path in temp_files_paths]
    for input_file_object, output_file_path in zip(input_files_objects, output_files_paths):
        input_file_object.set_output_file_path(output_file_path)
        input_file_object.converted = True
    return input_files_objects
        

