import sys
sys.path.insert(0, '..')

from general import GeneralConverter
from xhtml2pdf import pisa
import html2text
from file_manager import FileManager
from utils import rename_filename_with_extension
from bs4 import BeautifulSoup
from config import UPLOAD_FOLDER
import os
import io

ABIWORD_CONVERT  = "abiword --to=pdf --to-name=%s %s"

class HtmlPdf(GeneralConverter):
    """
    This class is for Html-Pdf conversion.
    """
    def __init__(self, file_objects=[]):
        self.initial_format = 'html'
        self.final_format = 'pdf'
        self.file_batch = file_objects
        
    def _single_convert(self, input_file_object):
        if input_file_object:
            input_file_path = input_file_object.get_input_file_path()
            h = html2text.HTML2Text()
            h.ignore_links = h.ignore_images = True
            input_plain_text = h.handle(open(input_file_path).read())
            file_is_cjk = check_if_cjk(input_plain_text)
            output_file_name = rename_filename_with_extension(
                os.path.basename(input_file_path), 'html')
            if file_is_cjk:
                os.system(ABIWORD_CONVERT%(output_file_name, input_file_path))
            else:
                input_stream = input_file_object.get_input_stream()
                soup = BeautifulSoup(input_stream)
                invalidAttrs = 'href src width height target style color face size script'.split()
                for attr in invalidAttrs:
                    [s.extract() for s in soup(attr)]
                input_stream = unicode(soup)
                output_file_name = rename_filename_with_extension(
                    os.path.basename(input_file_object.get_input_file_path()),
                    self.final_format)
                output_file = io.open(output_file_name, 'w+b')
                try:
                    pisa.CreatePDF(bytestream, dest=output_file)
                except:
                    print "Conversion Unsuccessfull for html_pdf"
                    os.system('rm %s'%output_file_name)
                    return None
            try:
                open(output_file_name)
                os.system('mv %s %s'%(output_file_name, UPLOAD_FOLDER))
                return os.path.join(UPLOAD_FOLDER, output_file_name)
            except IOError:
                print "Conversion Unsuccessfull for html_pdf"
                return None
        else:
            return None

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

