import sys
sys.path.append('..')
sys.path.append('../..')

import unittest
from txt_html import TxtHtml
from file_manager import FileManager

class TxtHtmlTests(unittest.TestCase):

    def test2_txthtml1(self):
        file1 = FileManager('test_files/test1.txt')
        file2 = FileManager('test_files/test2.txt')
        file3 = FileManager('test_files/test3.txt')
        file4 = FileManager('test_files/test4.txt')

        test = TxtHtml([file1, file2, file3, file4])
        test.convert()
        self.failUnless(open('test_files/test1.html'))
        self.failUnless(open('test_files/test2.html'))
        self.failUnless(open('test_files/test3.html'))
        self.failUnless(open('test_files/test4.html'))

def main():
    unittest.main()

if __name__ == '__main__':
    main()
