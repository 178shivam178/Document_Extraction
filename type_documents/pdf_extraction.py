import pytesseract
from pathlib import Path
from src.llm_model import CheckInvoice
from pdf2image import convert_from_path

def get_pdf_text(pdf_path):
    pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

    all_text = "" 
    pages = convert_from_path(Path(pdf_path), poppler_path=r"C:/Program Files/poppler-21.11.0/Library/bin")
    for pageNum, imgBlob in enumerate(pages):
        text = pytesseract.image_to_string(imgBlob, lang='eng')
    return text

def PDFProcessing(pdf_filepath):
    try:
        raw_text = get_pdf_text(pdf_filepath)
        extracted_fields,document_type = CheckInvoice(raw_text)
        return extracted_fields,document_type
    except Exception as e:
        return {'error': 'An error occurred', 'details': str(e)}