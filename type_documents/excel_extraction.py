import pandas as pd
from llm_engine.model import CheckInvoice
from pathlib import Path

def get_excel_text(excel_path):
    if isinstance(excel_path, Path):
            excel_path = str(excel_path)
    xls = pd.ExcelFile(str(excel_path), engine='openpyxl')
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
        print(e)
        raise {'error': 'An error occurred', 'details': str(e)}