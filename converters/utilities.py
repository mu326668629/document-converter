import sys
import re
import os
import shutil
import logging as log

sys.path.append('..')

from config import OUTPUT_FOLDER, UPLOAD_FOLDER
PARENT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
TMP_DIR = os.path.join(PARENT_DIR, UPLOAD_FOLDER)

from html_pdf import HtmlPdf
from html_txt import HtmlTxt
from pdf_html import PdfHtml
from txt_html import TxtHtml
from doc_pdf import DocPdf
from ppt_pdf import PptPdf
from rtf_pdf import RtfPdf

from utils import get_file_extension

from file_manager import FileManager


AVAILABLE_CONVERTERS = [(HtmlPdf, 'htmlpdf'), (HtmlTxt, 'htmltxt'),
                        (PdfHtml, 'pdfhtml'), (TxtHtml, 'txthtml'),
                        (DocPdf, 'docpdf'), (PptPdf, 'pptpdf'),
                        (RtfPdf, 'rtfpdf'), ]


def class_selector(input_format, output_format, result=None):
    result = result or []
    if input_format == output_format:
        return result
    direct_converter = get_direct_converter(input_format, output_format)
    if direct_converter:
        result.append(direct_converter)
        return result
    input_regex = make_regex(input_format)
    input_matches = get_input_matches(input_regex)
    for input_match in input_matches:
        converter, converter_expression = input_match
        intermediate_format = get_intermediate_format(converter_expression,
                                                      input_format)
        result.append(input_match)
        converter_list = class_selector(intermediate_format, output_format,
                                        result)
        if converter_list:
            return converter_list
        else:
            result.pop()


def get_intermediate_format(converter_expression, input_format):
    return re.sub(input_format, '', converter_expression)


def get_input_matches(input_regex):
    return [(converter, expression)
            for converter, expression in AVAILABLE_CONVERTERS
            if input_regex.match(expression)]


def make_regex(format_string):
    return re.compile('^%s'%format_string)


def get_direct_converter(input_format, output_format):
    converter_expression = '%s%s'%(input_format, output_format)
    for converter, expression in AVAILABLE_CONVERTERS:
        if re.match(converter_expression, expression):
            return (converter, expression)


def get_input_format(input_files_objects):
    sample_input_file = input_files_objects[0].get_input_file_path()
    input_format = get_file_extension(sample_input_file)
    return input_format


def set_flags_of_file_objects(input_files_objects, output_files_objects):
    for input_file_object, output_file_object in zip(input_files_objects,
                                                     output_files_objects):
        if (not output_file_object) or output_file_object == input_file_object:
            input_file_object.converted = False
        else:
            output_file_name = os.path.basename(
                output_file_object.get_input_file_path())
            os.system('mv %s %s' % (
                output_file_object.get_input_file_path(), OUTPUT_FOLDER))
            input_file_object.set_output_file_path(
                os.path.join(OUTPUT_FOLDER, output_file_name))
            input_file_object.converted = True
    return input_files_objects


def get_files_objects(files_paths):
    files_objects = []
    for file_path in files_paths:
        if file_path:
            file_object = FileManager(None, input_file_path=file_path)
            files_objects.append(file_object)
        else:
            files_objects.append(None)
    return files_objects


def handle_failed_conversion(input_file):
    if not input_file or not os.path.isfile(input_file):
        return
    failed_conversion_dir = os.path.join(TMP_DIR, 'failed_conversions')
    if not os.path.isdir(failed_conversion_dir):
        os.makedirs(failed_conversion_dir)
    filename = os.path.basename(input_file)
    try:
        shutil.copyfile(input_file, os.path.join(failed_conversion_dir,
                                                 filename))
    except IOError, ie:
        log.error(ie)
