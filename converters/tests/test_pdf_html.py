import sys
sys.path.append('..')
sys.path.append('/test_files')

import unittest
from pdf_html import PdfHtml

class PdfHtmlTests(unittest.TestCase):
    def test1_pdfhtmlconversions(self):
        test = PdfHtml(['test1.pdf', 'test2.pdf', 'test3.pdf'])
        self.failUnless(test.convert() == ['test1.html', 'test2.html', 'test3.html'])

    def test2_pdfhtmlexists(self):
        test = PdfHtml(['test1.pdf', 'test2.pdf', 'test3.pdf'])
        self.failUnless(open('test1.html'))
        self.failUnless(open('test2.html'))
        self.failUnless(open('test3.html'))

def main():
    unittest.main()

if __name__ == '__main__':
    main()
