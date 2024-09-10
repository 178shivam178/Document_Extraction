from llm_engine.model import CheckInvoice

def get_txt_text(file_path):
    all_text=''
    with open(file_path, 'r') as f:
        content = f.read()
        all_text += content
    return all_text

def TxtProcessing(txt_filepath):
    try:
        raw_text = get_txt_text(txt_filepath)
        extracted_fields,document_type = CheckInvoice(raw_text)
        return extracted_fields,document_type
    except Exception as e:
        return {'error': 'An error occurred', 'details': str(e)}