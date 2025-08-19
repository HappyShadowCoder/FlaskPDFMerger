from flask import Flask, request, send_file, render_template
from PyPDF2 import PdfMerger
from pymongo import MongoClient
from datetime import datetime
import requests
import io
import os


APP_OFFLINE = False  # Set True to make the app offline
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), "templates"))

# Mongo Setup
client = MongoClient(os.getenv("MONGO_URI"))
db = client["pdf_merger_app"]
visitors_collection = db["visitors"]
admins_collection = db["admins"]

@app.before_request
def check_offline():
    if APP_OFFLINE and request.endpoint != "static":
        return render_template("offline.html")

@app.before_request
def log_ip_location():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    if ip and "," in ip:
        ip = ip.split(",")[0].strip()
    try:
        res = requests.get(f"https://ipinfo.io/{ip}?token={os.getenv('IPINFO_TOKEN')}")
        data = res.json()

        admin_user = admins_collection.find_one({"ip": ip})
        is_admin = admin_user is not None

        log_entry = {
            "city": data.get("city"),
            "region": data.get("region"),
            "country": data.get("country"),
            "org": data.get("org"),
            "loc": data.get("loc"),
            "is_admin": is_admin,
            "last_seen": datetime.utcnow()
        }

        visitors_collection.update_one(
            {"ip": ip},
            {
                "$set": log_entry,               # update location + admin info
                "$inc": {"visit_count": 1}       # increment visit count
            },
            upsert=True
        )

        print(f"Visitor logged/updated: {ip}")
    except Exception as e:
        print("Could not fetch/store location:", e)

@app.route("/", methods=["GET"])
def index():
    def index():
        if APP_OFFLINE:
            return render_template("offline.html")  # Show maintenance page
        return render_template("index.html")

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
