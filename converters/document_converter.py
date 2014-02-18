import sys
sys.path.append('..')

from utils import get_file_extension
from utilities import class_selector
from utilities import remove_duplicates
from file_manager import FileManager
from config import OUTPUT_FOLDER
import os

def convert(input_files_objects, output_formats):
    sample_input_file = input_files_objects[0].get_input_file_path()
    input_format = get_file_extension(sample_input_file)
    converters = [class_selector(input_format, output_format) for output_format in output_formats]
    converters = remove_duplicates(converters)
    interim_files_objects = input_files_objects
    for converter, expression in converters:
        obj = converter(interim_files_objects)
        interim_files_paths = obj.convert()
        [interim_file_object.remove_input_file() for interim_file_object in interim_files_objects if interim_file_object]
        interim_files_objects = []
        for interim_file_path in interim_files_paths:
            if interim_file_path:
                interim_files_objects.append(FileManager(None, input_file_path = interim_file_path))
            else:
                interim_files_objects.append(None)
    for i, interim_file_object in enumerate(interim_files_objects):
        if interim_file_object:
            output_file_name = os.path.basename(interim_file_object.get_input_file_path())
            os.system('mv %s %s'%(interim_file_object.get_input_file_path(), OUTPUT_FOLDER))
            input_files_objects[i].set_output_file_path(os.path.join(OUTPUT_FOLDER, output_file_name))
            input_files_objects[i].converted = True
    return input_files_objects

