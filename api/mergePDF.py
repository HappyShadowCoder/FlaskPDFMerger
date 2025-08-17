from flask import Flask, request, send_file
from PyPDF2 import PdfMerger
import io
import os

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates")
)

@app.route("/", methods=["GET", "POST"])
def merge_pdfs():
    if request.method == "POST":
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

    # GET request: show a simple upload form
    return '''
    <h2>Merge PDFs</h2>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="pdfs" multiple required>
        <button type="submit">Merge PDFs</button>
    </form>
    '''

if __name__ == "__main__":
    # Bind to 0.0.0.0 so Render can route to it
    app.run(host="0.0.0.0", port=5000)
