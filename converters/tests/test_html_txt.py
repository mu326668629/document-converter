import sys
sys.path.append('..')
sys.path.append('../..')

import unittest
from html_txt import HtmlTxt
from file_manager import FileManager

class HtmlTxtTests(unittest.TestCase):

    def test2_htmltxt1(self):
        file1 = FileManager('test_files/test1.html')
        file2 = FileManager('test_files/test2.html')
        file3 = FileManager('test_files/test3.html')
        file4 = FileManager('test_files/test4.html')

        test = HtmlTxt([file1, file2, file3, file4])
        test.convert()
        self.failUnless(open('test_files/test1.txt'))
        self.failUnless(open('test_files/test2.txt'))
        self.failUnless(open('test_files/test3.txt'))
        self.failUnless(open('test_files/test4.txt'))

    def test2_htmltxt2(self):
        file1 = FileManager('test_files/test1.html', '.')
        file2 = FileManager('test_files/test2.html', '.')
        file3 = FileManager('test_files/test3.html', '.')
        file4 = FileManager('test_files/test4.html', '.')

        test = HtmlTxt([file1, file2, file3, file4])
        test.convert()
        self.failUnless(open('test1.txt'))
        self.failUnless(open('test2.txt'))
        self.failUnless(open('test3.txt'))
        self.failUnless(open('test4.txt'))

def main():
    unittest.main()

if __name__ == '__main__':
    main()
