import sys
sys.path.append('..')
sys.path.append('./test_files')
sys.path.append('converters/')

import unittest
from file_manager import FileManager
from html_txt import HtmlTxt

file_manager1 = FileManager('tests/test_files/hello.html')
file_manager2 = FileManager('tests/test_files/not.html')

class FileManagerTests(unittest.TestCase):
    test = HtmlTxt()
    def FileManagerInputFileExistsTests(self):
        self.failUnless(isinstance(file_manager1.input_file_exists(), file))
        self.failUnless(isinstance(file_manager2.input_file_exists(), None))

    def FileManagerWriteTests(self):
        self.failUnless(isinstance(file_manager1.write('pdf', bytestream), file))

def main():
    unittest.main()

if __name__ == '__main__':
    main()
