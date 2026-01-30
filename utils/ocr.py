import pytesseract
import cv2
from pdf2image import convert_from_path

# Force Tesseract path (Windows-safe)
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def ocr_image(path: str) -> str:
    """
    OCR handler that supports:
    - PDF files (converted to images)
    - Image files (png/jpg)
    Always fails gracefully (returns empty string).
    """

    try:
        # Case 1: PDF -> images -> OCR
        if path.lower().endswith(".pdf"):
            images = convert_from_path(path, dpi=300)
            text = ""
            for img in images:
                text += pytesseract.image_to_string(img)
            return text.strip()

        # Case 2: Image file
        img = cv2.imread(path)
        if img is None:
            return ""

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return pytesseract.image_to_string(gray).strip()

    except Exception as e:
        print(f"[OCR ERROR] {e}")
        return ""
