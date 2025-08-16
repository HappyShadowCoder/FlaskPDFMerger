from flask import Flask, request, send_file
from PyPDF2 import PdfMerger
import io

app = Flask(__name__)

@app.route("/merge", methods=["POST"])
def merge_pdfs():
    files = request.files.getlist("pdfs")
    merger = PdfMerger()

    for f in files:
        merger.append(f.stream)

    output = io.BytesIO()
    merger.write(output)
    merger.close()
    output.seek(0)

    return send_file(output, as_attachment=True, download_name="Merged.pdf")

# Vercel handler
def handler(request, response):
    with app.test_request_context(
        path=request.path,
        method=request.method,
        data=request.data,
        headers=request.headers,
        query_string=request.query
    ):
        return app.full_dispatch_request()