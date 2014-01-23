import sys
sys.path.append('..')
sys.path.append('/test_files')

import unittest
from txt_html import TxtHtml

class TxtHtmlTests(unittest.TestCase):
    def test1_txthtmlconversions(self):
        test = TxtHtml('test1.txt', 'test2.txt', 'test3.txt')
        self.failUnless(test.batch_convert() == ['test1.html', 'test2.html', 'test3.html'])

    def test2_txthtmlexists(self):
        test = TxtHtml('test1.txt', 'test2.txt', 'test3.txt')
        self.failUnless(open('test1.html'))
        self.failUnless(open('test2.html'))
        self.failUnless(open('test3.html'))

def main():
    unittest.main()

if __name__ == '__main__':
    main()
