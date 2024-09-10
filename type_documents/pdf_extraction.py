import pytesseract
from pathlib import Path
from llm_engine.model import CheckInvoice
from pdf2image import convert_from_path

# Custom exceptions
class PDFProcessingError(Exception):
    def __init__(self, message, details=""):
        super().__init__(message)
        self.details = details

def get_pdf_text(pdf_path: str) -> str:
    pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files (x86)/Tesseract-OCR/tesseract.exe"
    poppler_path = "dependency/poppler-21.11.0/Library/bin"
    
    all_text = ""
    try:
        pages = convert_from_path(Path(pdf_path), poppler_path=poppler_path)
    except Exception as e:
        print(e)
        raise PDFProcessingError('Failed to convert PDF to images', str(e))

    for page_num, img_blob in enumerate(pages):
        try:
            text = pytesseract.image_to_string(img_blob, lang='eng')
            all_text += text + "\n"
        except Exception as e:
            print(e)
            raise PDFProcessingError(f'Failed to extract text from page {page_num}', str(e))
    
    return all_text

def PDFProcessing(pdf_filepath: str):
    try:
        raw_text = get_pdf_text(pdf_filepath)
        extracted_fields, document_type = CheckInvoice(raw_text)
        return extracted_fields, document_type
    except PDFProcessingError as e:
        # Specific handling for PDF processing errors
        print(f"PDF Processing Error: {e}")
        return {'error': str(e), 'details': e.details}
    except Exception as e:
        # General exception handling
        print(f"An unexpected error occurred: {str(e)}")
        return {'error': 'An error occurred', 'details': str(e)}
