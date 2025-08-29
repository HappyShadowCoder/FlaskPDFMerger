from flask import Blueprint, request, send_file, jsonify
from weasyprint import HTML
import io
import os

file_converter_bp = Blueprint('file_converter', __name__)

@file_converter_bp.route('/api/file-to-pdf', methods=['POST'])
def convert_file_to_pdf():
    """
    Receives an uploaded HTML file, injects CSS, and converts to PDF.
    """
    if 'html_file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['html_file']
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    if file and file.filename.endswith('.html'):
        try:
            html_content = file.read().decode('utf-8')

            css_path = os.path.join(os.path.dirname(__file__), 'static', 'jupyter_classic.css')
            with open(css_path, 'r') as css_file:
                jupyter_css = css_file.read()
            
            if '</head>' in html_content:
                html_with_css = html_content.replace(
                    '</head>', 
                    f'<style>{jupyter_css}</style></head>'
                )
            else:
                html_with_css = f"<html><head><style>{jupyter_css}</style></head><body>{html_content}</body></html>"

            pdf_bytes = HTML(string=html_with_css).write_pdf()
            pdf_file = io.BytesIO(pdf_bytes)
            pdf_file.seek(0)
            
            return send_file(
                pdf_file,
                as_attachment=True,
                download_name=f"{os.path.splitext(file.filename)[0]}.pdf",
                mimetype='application/pdf'
            )

        except Exception as e:
            print(f"Error during file conversion: {e}")
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    else:
        return jsonify({"error": "Invalid file type. Please upload an HTML file."}), 400

