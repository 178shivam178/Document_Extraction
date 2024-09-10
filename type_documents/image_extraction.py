from pathlib import Path
import easyocr
from llm_engine.model import CheckInvoice

def get_image_text(image_path):
    try:
        if isinstance(image_path, Path):
            image_path = str(image_path)
        
        reader = easyocr.Reader(['en'])
        extracted_text = reader.readtext(image_path, detail=0)  
        combined_text = ' '.join(extracted_text)
        return combined_text
    except Exception as e:
        raise f"Error in get_image_text: {e}"

def ImageProcessing(image_filepath):
    try:
        raw_text = get_image_text(image_filepath)
        
        if not isinstance(raw_text, str):
            raise TypeError("Expected raw_text to be a string")
        
        extracted_fields, document_type = CheckInvoice(raw_text)
        return extracted_fields, document_type
    except Exception as e:
        raise {'error': 'An error occurred', 'details': str(e)}
