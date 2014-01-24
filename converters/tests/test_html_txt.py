import sys
sys.path.append('..')
sys.path.append('/test_files')

import unittest
from html_txt import HtmlTxt

class HtmlTxtTests(unittest.TestCase):
    def test1_htmltxtconversions(self):
        test = HtmlTxt(['test1.html', 'test2.html', 'test3.html'])
        self.failUnless(test.convert() == ['test1.txt', 'test2.txt', 'test3.txt'])

    def test2_htmlpdfexists(self):
        test = HtmlTxt(['test1.html', 'test2.html', 'test3.html'])
        self.failUnless(open('test1.txt'))
        self.failUnless(open('test2.txt'))
        self.failUnless(open('test3.txt'))

def main():
    unittest.main()

if __name__ == '__main__':
    main()
