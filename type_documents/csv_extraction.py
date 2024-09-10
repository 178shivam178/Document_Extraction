import pandas as pd
from src.llm_model import CheckInvoice
def get_csv_text(csv_path):
    data_frame = pd.read_csv(csv_path)
    all_text = ''

    for _, row in data_frame.iterrows():
        document = ' '.join(str(cell) for cell in row)
        all_text += document + '\n'

    return all_text

def CSVProcessing(csv_filepath):
    try:
        raw_text = get_csv_text(csv_filepath)
        extracted_fields,document_type = CheckInvoice(raw_text)
        return extracted_fields,document_type

    except Exception as e:
        return {'error': 'An error occurred', 'details': str(e)}
