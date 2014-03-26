import unittest

from utilities import class_selector
from utilities import get_intermediate_format

from html_pdf import HtmlPdf
from html_txt import HtmlTxt
from pdf_html import PdfHtml
from txt_html import TxtHtml
from doc_pdf import DocPdf
from ppt_pdf import PptPdf


class TestClassSelector(unittest.TestCase):


    def setUp(self):
        pass


    def test_class_selector_same(self):
        self.assertEqual(class_selector('pdf', 'pdf'), [])
        self.assertEqual(class_selector('html', 'html'), [])
        self.assertEqual(class_selector('txt', 'txt'), [])
        self.assertEqual(class_selector('doc', 'doc'), [])


    def test_class_selector_direct(self):
        self.assertEqual(class_selector('pdf', 'html'), [(PdfHtml, 'pdfhtml')])
        self.assertEqual(class_selector('html', 'pdf'), [(HtmlPdf, 'htmlpdf')])
        self.assertEqual(class_selector('html', 'txt'), [(HtmlTxt, 'htmltxt')])
        self.assertEqual(class_selector('doc', 'pdf'), [(DocPdf, 'docpdf')])
        self.assertEqual(class_selector('txt', 'html'), [(TxtHtml, 'txthtml')])
        self.assertEqual(class_selector('ppt', 'pdf'), [(PptPdf, 'pptpdf')])


    def test_class_selector_chain(self):
        self.assertEqual(class_selector('pdf', 'txt'), [(PdfHtml, 'pdfhtml'), (HtmlTxt, 'htmltxt')])
        self.assertEqual(class_selector('txt', 'pdf'), [(TxtHtml, 'txthtml'), (HtmlPdf, 'htmlpdf')])
        self.assertEqual(class_selector('doc', 'html'), [(DocPdf, 'docpdf'), (PdfHtml, 'pdfhtml')])
        self.assertEqual(class_selector('doc', 'txt'), [(DocPdf, 'docpdf'), (PdfHtml, 'pdfhtml'),
                                                         (HtmlTxt, 'htmltxt')])
        self.assertEqual(class_selector('ppt', 'html'), [(PptPdf, 'pptpdf'), (PdfHtml, 'pdfhtml')])
        self.assertEqual(class_selector('ppt', 'txt'), [(PptPdf, 'pptpdf'), (PdfHtml, 'pdfhtml'),
                                                        (HtmlTxt, 'htmltxt')])


class TestGetIntermediateFormat(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_intermediate_format(self):
        self.assertEqual(get_intermediate_format('pdfhtml', 'pdf'), 'html')
        self.assertEqual(get_intermediate_format('htmlpdf', 'html'), 'pdf')
        self.assertEqual(get_intermediate_format('txthtml', 'txt'), 'html')
        self.assertEqual(get_intermediate_format('docpdf', 'doc'), 'pdf')
        self.assertEqual(get_intermediate_format('pdfhtml', 'pdf'), 'html')


if __name__ == '__main__':
    unittest.main()
