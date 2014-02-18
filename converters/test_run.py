from document_converter import convert
from file_manager import FileManager

file1 = FileManager('input/6.pdf')
file2 = FileManager('input/3.html')
file3 = FileManager('input/1.txt')

convert([file1], ['txt'])
convert([file3], ['pdf'])
