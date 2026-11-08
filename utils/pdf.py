"""PDF text extraction with repair and optional per-page OCR."""
import io
import os
import shutil

import pdfplumber
import pypdfium2 as pdfium


def extract_text_from_pdf(path: str) -> str:
    """Read actual page contents; fail explicitly if any page is unreadable."""
    with pdfium.PdfDocument(str(path)) as document:
        if not len(document):
            raise ValueError('PDF contains no pages')
        # Re-save through PDFium to repair malformed cross-reference tables.
        repaired = io.BytesIO()
        document.save(repaired)
        repaired.seek(0)
        texts = []
        with pdfplumber.open(repaired) as pdf:
            for index, page in enumerate(pdf.pages):
                text = page.extract_text() or ''
                if not text.strip():
                    import pytesseract
                    command = os.environ.get('TESSERACT_CMD') or shutil.which('tesseract')
                    if not command:
                        raise ValueError(f'Page {index + 1} needs OCR; install Tesseract and add it to PATH or set TESSERACT_CMD')
                    pytesseract.pytesseract.tesseract_cmd = command
                    image = document[index].render(scale=3).to_pil()
                    try:
                        text = pytesseract.image_to_string(image, timeout=60)
                    finally:
                        image.close()
                    if not text.strip():
                        raise ValueError(f'No readable text on page {index + 1}')
                texts.append(text)
    return '\n'.join(texts)
