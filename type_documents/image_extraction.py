from src.llm_model import CheckInvoice
import easyocr


def get_image_text(image_path):
    reader = easyocr.Reader(['en'])
    extracted_text = reader.readtext(image_path, detail=0)
    combined_text = ' '.join(extracted_text)

    return combined_text

def ImageProcessing(image_filepath):
    try:
        raw_text = get_image_text(str(image_filepath))
        extracted_fields,document_type = CheckInvoice(raw_text)
        return extracted_fields,document_type
    except Exception as e:
        return {'error': 'An error occurred', 'details': str(e)}