import sys
sys.path.append('..')
sys.path.append('../..')

import unittest
from html_pdf import HtmlPdf
from file_manager import FileManager


class HtmlPdfTests(unittest.TestCase):

    def test2_htmlpdf1(self):
        file1 = FileManager('test_files/test1.html')
        file2 = FileManager('test_files/test2.html')
        file3 = FileManager('test_files/test3.html')

        test = HtmlPdf([file1, file2, file3])
        test.convert()
        self.failUnless(open('test_files/test1.pdf'))
        self.failUnless(open('test_files/test2.pdf'))
        self.failUnless(open('test_files/test3.pdf'))

    def test2_htmlpdf2(self):
        file1 = FileManager('test_files/test1.html', '.')
        file2 = FileManager('test_files/test2.html', '.')
        file3 = FileManager('test_files/test3.html', '.')

        test = HtmlPdf([file1, file2, file3])
        test.convert()
        self.failUnless(open('test1.pdf'))
        self.failUnless(open('test2.pdf'))
        self.failUnless(open('test3.pdf'))

def main():
    unittest.main()

if __name__ == '__main__':
    main()
