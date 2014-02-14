import sys
sys.path.append('..')

from html_pdf import HtmlPdf
from html_txt import HtmlTxt
from pdf_html import PdfHtml
from txt_html import TxtHtml
from doc_html import DocHtml
from doc_pdf import DocPdf
import re


AVAILABLE_FORMATS = ['pdf', 'html', 'txt', 'doc']

AVAILABLE_CONVERTERS = [(HtmlPdf, 'htmlpdf'), (HtmlTxt, 'htmltxt'), (PdfHtml, 'pdfhtml'),
                        (TxtHtml, 'txthtml'), (DocHtml, 'dochtml'), (DocPdf, 'docpdf')]

FORMAT_RE = [re.compile('.*%s'%fmt) for fmt in AVAILABLE_FORMATS]

def class_selector(input_format, output_format):
    input_format_re = re.compile('^%s.*$'%input_format)
    output_format_re = re.compile('^.*%s$'%output_format)
    converter1 = [(converter, expression) for converter, expression in AVAILABLE_CONVERTERS
                  if input_format_re.match(expression)]
    converter2 = [(converter, expression) for converter, expression in AVAILABLE_CONVERTERS
                  if output_format_re.match(expression)]
    converters = list(set(converter1) & set(converter2))
    if not converters:
        input_re = re.compile('^%s'%input_format)
        interim_formats = [input_re.sub('', expression) for converter, expression in converter1]
        for i, interim_format in enumerate(interim_formats):
            converters = class_selector(interim_format, output_format)
            if converters:
                converters = [converter1[i], converters]
    return converters

def remove_duplicates(converters_list):
    product = []
    for converter_list in converters_list:
        for converter in converter_list:
            if converter not in product:
                product.append(converter)    
    return product

def check_if_cjk(str):
    '''
    rudimentary CJK detection
    seems like a lot of it is between these two ranges.
    cf. http://www.alanwood.net/unicode/fontsbyrange.html
    '''
    ranges = [(12272, 12287), (19968, 40959)]
    for i in str:
        j = ord(i)
        for (low, high) in ranges:
            if j > low and j < high:
                return True
    return False
