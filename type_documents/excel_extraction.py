import pandas as pd
from src.llm_model import CheckInvoice

def get_excel_text(excel_path):
    xls = pd.ExcelFile(excel_path, engine='openpyxl')
    all_text = ''

    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name)
        for _, row in df.iterrows():
            document = ' '.join(str(cell) for cell in row)
            all_text += document + '\n'  # Add a newline after each row

    return all_text

def ExcelProcessing(excel_filepath):
    try:
        raw_text = get_excel_text(excel_filepath)
        extracted_fields,document_type = CheckInvoice(raw_text)
        return extracted_fields,document_type

    except Exception as e:
        return {'error': 'An error occurred', 'details': str(e)}