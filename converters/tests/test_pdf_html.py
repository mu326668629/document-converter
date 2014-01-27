import sys
sys.path.insert('..')
sys.path.insert('../..')

import unittest
from pdf_html import PdfHtml
from file_manager import FileManager

class PdfHtmlTests(unittest.TestCase):
    def test1_pdfhtmlconversions(self):

    def test2_pdfhtml1(self):
        file1 = FileManager('test_files/test1.pdf')
        file2 = FileManager('test_files/test2.pdf')
        file3 = FileManager('test_files/test3.pdf')
        file4 = FileManager('test_files/test4.pdf')

        test = PdfHtml([file1, file2, file3, file4])
        test.convert()
        self.failUnless(open('test_files/test1.html'))
        self.failUnless(open('test_files/test2.html'))
        self.failUnless(open('test_files/test3.html'))
        self.failUnless(open('test_files/test4.html'))

    def test2_txthtml2(self):
        file1 = FileManager('test_files/test1.pdf', 'test_files')
        file2 = FileManager('test_files/test2.pdf', 'test_files')
        file3 = FileManager('test_files/test3.pdf', 'test_files')
        file4 = FileManager('test_files/test4.pdf', 'test_files')

        test = TxtHtml([file1, file2, file3])
        test.convert()
        self.failUnless(open('test1.html'))
        self.failUnless(open('test2.html'))
        self.failUnless(open('test3.html'))
        self.failUnless(open('test4.html'))

def main():
    unittest.main()

if __name__ == '__main__':
    main()
