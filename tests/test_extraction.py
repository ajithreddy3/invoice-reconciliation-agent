import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.graph import app
from agents.document_agent import document_agent
from utils.invoice_parser import parse_invoice
from utils.pdf import extract_text_from_pdf
from utils.schemas import AgentState

ROOT = Path(__file__).resolve().parents[1]


def write_pdf(path, total='12.00'):
    # A real one-page text PDF, independent of the bundled fixtures and filenames.
    lines = ['Example Supplies', 'Invoice Number: NEW-123', 'Invoice Date: 2026-11-09',
             'Currency: GBP', 'Description Quantity Unit Price Total',
             'Widget 2 pcs 5.00 10.00', 'Subtotal: 10.00', 'VAT: 2.00', f'Total: {total}']
    content = ('BT /F1 12 Tf 50 780 Td 18 TL ' + ' '.join(f'({line}) Tj T*' for line in lines) + ' ET').encode()
    objects = [b'<< /Type /Catalog /Pages 2 0 R >>',
               b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
               b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>',
               b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',
               b'<< /Length ' + str(len(content)).encode() + b' >>\nstream\n' + content + b'\nendstream']
    data = b'%PDF-1.4\n'
    offsets = [0]
    for number, obj in enumerate(objects, 1):
        offsets.append(len(data))
        data += f'{number} 0 obj\n'.encode() + obj + b'\nendobj\n'
    start = len(data)
    data += b'xref\n0 6\n0000000000 65535 f \n'
    data += b''.join(f'{offset:010d} 00000 n \n'.encode() for offset in offsets[1:])
    data += f'trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n{start}\n%%EOF'.encode()
    path.write_bytes(data)


class ExtractionTests(unittest.TestCase):
    def test_renamed_pdf_same_content(self):
        source = ROOT / 'data/invoices/Invoice_1_Baseline.pdf'
        with tempfile.TemporaryDirectory() as folder:
            renamed = Path(folder) / 'unseen-name.pdf'
            shutil.copyfile(source, renamed)
            original = document_agent(AgentState(filename=str(source)))
            copied = document_agent(AgentState(filename=str(renamed)))
        self.assertEqual(original.extracted_invoice, copied.extracted_invoice)
        self.assertEqual(copied.extracted_invoice.total, 9573)
        self.assertEqual(copied.extracted_invoice.currency, 'GBP')

    def test_new_pdf_and_changed_contents(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'new.pdf'
            write_pdf(path)
            invoice = document_agent(AgentState(filename=str(path)))
            self.assertEqual(invoice.extracted_invoice.invoice_number, 'NEW-123')
            self.assertEqual(invoice.extracted_invoice.total, 12)
            self.assertEqual(invoice.extracted_invoice.line_items[0].quantity, 2)
            self.assertFalse(invoice.discrepancies)
            write_pdf(path, total='13.00')
            changed = app.invoke(AgentState(filename=str(path)))
            self.assertEqual(changed['extracted_invoice'].total, 13)
            self.assertEqual(changed['recommended_action'], 'flag_for_review')
            self.assertTrue(any(d.type == 'extraction_incomplete' for d in changed['discrepancies']))

    def test_bundled_text_layouts_and_repair(self):
        for filename, number, count in [('Invoice_1_Baseline.pdf', 'INV-2024-1001', 4),
                                        ('Invoice_3_Different_Format.pdf', 'MC-INV-3421', 4),
                                        ('Invoice_4_Price_Trap.pdf', 'GPS-8842', 3),
                                        ('Invoice_5_Missing_PO.pdf', 'EC-7721', 4)]:
            with self.subTest(filename=filename):
                state = document_agent(AgentState(filename=str(ROOT / 'data/invoices' / filename)))
                self.assertFalse(state.discrepancies)
                self.assertEqual(state.extracted_invoice.invoice_number, number)
                self.assertEqual(len(state.extracted_invoice.line_items), count)

    def test_sample_decisions(self):
        for filename, expected in [('Invoice_1_Baseline.pdf', 'auto_approve'),
                                   ('Invoice_3_Different_Format.pdf', 'auto_approve'),
                                   ('Invoice_4_Price_Trap.pdf', 'flag_for_review'),
                                   ('Invoice_5_Missing_PO.pdf', 'flag_for_review')]:
            with self.subTest(filename=filename):
                result = app.invoke(AgentState(filename=str(ROOT / 'data/invoices' / filename)))
                self.assertEqual(result['recommended_action'], expected)

    def test_scanned_without_ocr_requires_review(self):
        with patch('utils.pdf.shutil.which', return_value=None), patch.dict('os.environ', {}, clear=True):
            result = app.invoke(AgentState(filename=str(ROOT / 'data/invoices/Invoice_2_Scanned.pdf')))
        self.assertEqual(result['recommended_action'], 'flag_for_review')
        self.assertIsNone(result.get('extracted_invoice'))
        self.assertIn('needs OCR', result['discrepancies'][0].details)

    def test_ocr_page_fallback(self):
        with patch('utils.pdf.shutil.which', return_value='tesseract'), patch('pytesseract.image_to_string', return_value='Invoice OCR text'):
            self.assertEqual(extract_text_from_pdf(str(ROOT / 'data/invoices/Invoice_2_Scanned.pdf')), 'Invoice OCR text')

    def test_missing_and_invalid_files_require_review(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'invalid.pdf'
            for contents in (None, b'not a PDF'):
                if contents is not None:
                    path.write_bytes(contents)
                result = app.invoke(AgentState(filename=str(path)))
                self.assertEqual(result['recommended_action'], 'flag_for_review')
                self.assertEqual(result['discrepancies'][0].type, 'extraction_failed')

    def test_incomplete_extraction_is_not_confident(self):
        invoice, issues = parse_invoice('Unknown Vendor\nTotal: 0.00')
        self.assertTrue(issues)
        self.assertEqual(invoice.currency, 'UNKNOWN')


if __name__ == '__main__':
    unittest.main()
