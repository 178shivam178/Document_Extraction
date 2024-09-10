import os
import logging
from flask import Flask, Blueprint, jsonify, request, make_response, send_from_directory
from werkzeug.utils import secure_filename
from type_documents.pdf_extraction import PDFProcessing
from type_documents.image_extraction import ImageProcessing
from type_documents.docx_extraction import DocxProcessing
from type_documents.csv_extraction import CSVProcessing
from type_documents.excel_extraction import ExcelProcessing
from type_documents.txt_extraction import TxtProcessing
from llm_engine.model import CheckInvoice

class FileProcessingError(Exception):
    pass

class InvalidFileError(FileProcessingError):
    pass

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def create_app():
    app = Flask(__name__)
    uploads_folder = os.environ.get('UPLOAD_FOLDER', 'uploads')
    if not os.path.exists(uploads_folder):
        os.makedirs(uploads_folder)
    app.config['UPLOAD_FOLDER'] = uploads_folder
    app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
    app.config['ALLOWED_EXTENSIONS'] = set(os.environ.get('ALLOWED_EXTENSIONS', 'csv,png,jpeg,jpg,pdf,docx,xlsx,txt').split(','))
    app.config['LOG_FILE'] = os.environ.get('LOG_FILE', 'logs/app.log')

    logging.basicConfig(filename=app.config['LOG_FILE'], level=logging.ERROR)

    api_bp = Blueprint('api', __name__)

    @api_bp.route('/v1/api/extraction', methods=['POST'])
    def ExtractionAPI():
        try:
            file = request.files.get('file')
            text = request.form.get('text')

            if file and text:
                raise InvalidFileError('Both file and text input provided. Please provide either a file or text, but not both.')

            if file:
                if not allowed_file(file.filename):
                    raise InvalidFileError('Invalid file type')

                filepath = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filepath))

                file_extension = filepath.rsplit('.', 1)[1].lower()
                # name = filepath.rsplit('.', 1)[0]

                doc_path = os.path.join(app.config['UPLOAD_FOLDER'], filepath)

                if file_extension == 'pdf':
                    print(f"Performing extraction on PDF file: {filepath}")
                    extracted_fields,document_type = PDFProcessing(doc_path)

                elif file_extension in {'png', 'jpeg', 'jpg'}:
                    print(f"Performing processing on image file: {filepath}")
                    extracted_fields,document_type = ImageProcessing(doc_path)

                elif file_extension == 'docx':
                    print(f"Performing processing on Doc file: {filepath}")
                    extracted_fields,document_type = DocxProcessing(doc_path)

                elif file_extension == 'xlsx':
                    print(f"Performing processing on Excel file: {filepath}")
                    extracted_fields,document_type = ExcelProcessing(doc_path)

                elif file_extension == 'csv':
                    print(f"Performing processing on image file: {filepath}")
                    extracted_fields,document_type = CSVProcessing(doc_path)

                elif file_extension == 'txt':
                    print(f"Performing processing on image file: {filepath}")
                    extracted_fields,document_type = TxtProcessing(doc_path)

                else:
                    raise InvalidFileError(f'Error: cannot process {file_extension} files')
            elif text:
                print(f"Performing processing on text input: {text}")
                extracted_fields,document_type = CheckInvoice(text)
            else:
                raise InvalidFileError('No file or text input provided')
            
            extracted_fields["document_type"] = document_type
            return jsonify(extracted_fields)

        except InvalidFileError as e:
            return make_response(jsonify({'error': str(e)}), 400)

        except Exception as e:
            logging.error(f'Error: {str(e)}')
            return make_response(jsonify({'error': f'An unexpected error occurred during processing {e}'}), 500)

    app.register_blueprint(api_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=3008,debug=True)
