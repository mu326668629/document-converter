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
    input_format_re = re.compile('%s.*'%input_format)
    output_format_re =  re.compile('.*%s'%output_format)
    result = [(converter, expression) for converter, expression in AVAILABLE_CONVERTERS
              if input_format_re.match(expression) and output_format_re.match(expression)]
    if not result:
        result1 = [(converter, expression) for converter, expression in AVAILABLE_CONVERTERS
                   if input_format_re.match(expression)]
        result2 = [(converter, expression) for converter, expression in AVAILABLE_CONVERTERS
                   if output_format_re.match(expression)]
        for converter, expression in result1:
            result.append((converter, expression))
            input_format_c = expression[len(input_format):]
            input_format_c_re = re.compile('%s.*'%input_format_c)
            if not class_selector(input_format_c, output_format):
                result = result[:-1]
            else:
                result.append(class_selector(input_format_c, output_format)[0])
    return result

def remove_duplicates(converters_list):
    product = []
    for converter_list in converters_list:
        for converter in converter_list:
            if converter not in product:
                product.append(converter)    
    return product
