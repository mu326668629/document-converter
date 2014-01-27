import sys
sys.path.append('..')
sys.path.append('../..')

import unittest

from document_converter import convert
from file_manager import FileManager

class ConvertTests(unittest.TestCase):
    def test1_converttest(self):
        file1 = FileManager('test_files/test1.html')
        file2 = FileManager('test_files/test2.html')
        file3 = FileManager('test_files/test3.html')
        file4 = FileManager('test_files/test4.html')
        convert([file1, file2, file3, file4], ['pdf', 'txt'])

        self.failUnless(open('test_files/test1.pdf'))
        self.failUnless(open('test_files/test2.pdf'))
        self.failUnless(open('test_files/test3.pdf'))
        self.failUnless(open('test_files/test4.pdf'))





def main():
    unittest.main()

if __name__ == '__main__':
    main()
