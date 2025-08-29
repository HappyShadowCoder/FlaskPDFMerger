from flask import Blueprint , request , send_file
from weasyprint import HTML
import io

html_converter_bp = Blueprint('html_converter', __name__)

@html_converter_bp.route('/api/html-to-pdf', methods=['POST'])
def convert_html_to_pdf():
    html_content = request.form.get('html_content')
    if not html_content:
        return "No HTML content provided", 400
    try:
        pdf_bytes = HTML(string=html_content).write_pdf()
        pdf_file = io.BytesIO(pdf_bytes)
        pdf_file.seek(0)
        return send_file(
        pdf_file,
        as_attachment=True,
        download_name="converted.pdf",
        mimetype='application/pdf'
        )
    except Exception as e :
        print(f"Error converting HTML to PDF with WeasyPrint: {e}")
        return "An error occurred during PDF conversion.", 500
