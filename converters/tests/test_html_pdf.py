import sys
sys.path.append('..')
sys.path.append('/test_files')

import unittest
from html_pdf import HtmlPdf

class HtmlPdfTests(unittest.TestCase):
    def test1_htmlpdfconversions(self):
        test = HtmlPdf(['test1.html', 'test2.html', 'test3.html'])
        self.failUnless(test.convert() == ['test1.pdf', 'test2.pdf', 'test3.pdf'])


    def test2_htmlpdfexists(self):
        test = HtmlPdf(['test1.html', 'test2.html', 'test3.html'])
        self.failUnless(open('test1.pdf'))
        self.failUnless(open('test2.pdf'))
        self.failUnless(open('test3.pdf'))

def main():
    unittest.main()

if __name__ == '__main__':
    main()
