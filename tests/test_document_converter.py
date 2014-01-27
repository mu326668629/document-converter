import sys
sys.path.append('..')
sys.path.append('../converters')
sys.path.append('test_files')


import unittest

from document_converter import convert

class ConvertTests(unittest.TestCase):
    def test1_converttest(self):
        #Note: test4.html contains javascript so this test also demonstrates
        #stripping of <script> elements.
        self.failUnless(
            convert(['test1.html', 'test2.html', 'test3.html', 'test4.html'],
                    ['pdf', 'txt']) ==
            [['test1.pdf', 'test2.pdf', 'test3.pdf', 'test4.pdf'], 
             ['test1.txt', 'test2.txt', 'test3.txt', 'test4.txt']])


def main():
    unittest.main()

if __name__ == '__main__':
    main()
