from flask import Flask , request , send_file , render_template
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
import io
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/merge" , methods = ["POST"])
def merge_pdfs():
    files = request.files.getlist("pdfs")
    merger = PdfMerger()

    for f in files:
        merger.append(f.stream)

    output = io.BytesIO() #
    merger.write(output)
    merger.close()
    output.seek(0)

    return send_file(output , as_attachment=True , download_name="Merged.pdf")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

