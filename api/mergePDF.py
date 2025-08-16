from flask import Flask, request, send_file
from PyPDF2 import PdfMerger
import io

app = Flask(__name__)

@app.route("/api/merge", methods=["POST"])
def merge_pdfs():
    files = request.files.getlist("pdfs")
    if len(files) < 2:
        return "Please upload at least two PDFs", 400

    merger = PdfMerger()
    for f in files:
        merger.append(f.stream)

    output = io.BytesIO()
    merger.write(output)
    merger.close()
    output.seek(0)

    return send_file(output, as_attachment=True, download_name="merged.pdf")

# Vercel expects this at the bottom
if __name__ == "__main__":
    app.run()
