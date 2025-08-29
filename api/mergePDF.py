from flask import Flask, request, send_file, render_template, jsonify
from PyPDF2 import PdfMerger
from pymongo import MongoClient
from datetime import datetime
import requests
import io
import os
from werkzeug.middleware.proxy_fix import ProxyFix
from api.html2pdf import html_converter_bp

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), "templates"))
app.register_blueprint(html_converter_bp)

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

client = MongoClient(os.getenv("MONGO_URI"))
db = client["pdf_merger_app"]
visitors_collection = db["visitors"]
admins_collection = db["admins"]

APP_OFFLINE = False

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
            {"$set": log_entry, "$inc": {"visit_count": 1}},
            upsert=True
        )
    except Exception as e:
        print("Could not fetch/store location:", e)

@app.before_request
def check_offline():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    if ip and "," in ip:
        ip = ip.split(",")[0].strip()
    admin_user = admins_collection.find_one({"ip": ip})
    is_admin = admin_user is not None
    if APP_OFFLINE and not is_admin and request.endpoint != "static":
        return render_template("offline.html")

@app.route("/", methods=["GET"])
def index():
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

@app.route("/api/check_admin", methods=["GET"])
def check_admin():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    if ip and "," in ip:
        ip = ip.split(",")[0].strip()
    admin_user = admins_collection.find_one({"ip": ip})
    is_admin = admin_user is not None
    return jsonify({"is_admin": is_admin})

@app.route("/admin/toggle_offline", methods=["POST"])
def toggle_offline():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    if ip and "," in ip:
        ip = ip.split(",")[0].strip()
    admin_user = admins_collection.find_one({"ip": ip})
    if not admin_user:
        return jsonify({"error": "Unauthorized"}), 403
    global APP_OFFLINE
    APP_OFFLINE = not APP_OFFLINE
    status = "offline" if APP_OFFLINE else "online"
    return jsonify({"message": f"App is now {status}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)