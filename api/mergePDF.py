from flask import Flask, request, send_file, render_template
from PyPDF2 import PdfMerger
import io
import os

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates")
)

@app.route("/", methods=["GET"])
def index():
    # This route serves the index.html file
    return render_template("index.html")

@app.route("/api/merge", methods=["POST"])
def merge_pdfs():
    # This route handles the POST request from the frontend to merge PDFs
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)