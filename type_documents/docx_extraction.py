import aspose.words as aw
from llm_engine.model import CheckInvoice
def get_docx_text(docx_file_path):
    doc = aw.Document(docx_file_path)
    all_text = ""
    for paragraph in doc.get_child_nodes(aw.NodeType.PARAGRAPH, True):
        all_text += paragraph.get_text() + "\n"
    return all_text

def DocxProcessing(docx_filepath):
    try:
        raw_text = get_docx_text(str(docx_filepath))
        extracted_fields,document_type = CheckInvoice(raw_text)
        return extracted_fields,document_type

    except Exception as e:
        return {'error': 'An error occurred', 'details': str(e)}
