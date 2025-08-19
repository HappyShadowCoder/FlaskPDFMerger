# Flask PDF Merger

A lightweight and user-friendly web application to seamlessly merge multiple PDF files into a single document. This project provides a clean and intuitive interface for PDF consolidation, making it perfect for personal or professional use.
***

## 🚀 Live Deployment

This Flask PDF Merger is deployed on **Render** and accessible publicly. You can use the app directly from your browser.

**Live App URL:** https://pdfmerger-atov.onrender.com

> 🧭 **Heads-up for Brave Browser Users**  
> Some users have reported that the app doesn't load properly in Brave due to its strict default settings.  
> While our app doesn't use trackers, Brave's aggressive blocking may interfere with normal functionality.  
> If you run into issues, try using Chrome, Firefox, or Edge for a smoother experience.



***

### ✨ Features

- **Merge Multiple PDFs:** Combine several PDF files into one with a single click.
- **Web Interface:** Upload PDFs directly through your browser without installing additional software.
- **Fast & Lightweight:** Built to be quick and efficient, even with multiple PDFs.
- **Download Merged PDF:** Receive the merged PDF instantly after processing.
- **Cross-Platform:** Works on any system with Python installed.
- **Easy Deployment:** Deploy locally or on cloud platforms like Heroku or Render.

***

### 🛠️ Tech Stack

This project is built with the following technologies:

- **Backend:** Python, Flask
- **PDF Processing:** PyPDF2
- **Frontend:** HTML, CSS (Jinja2 templates)
- **Server:** WSGI / Flask development server

***

### 🚀 How It Works

This is a web application where users can upload multiple PDFs, which are then merged into a single file using **PyPDF2**:

- **Upload PDFs:** Users select multiple PDF files through the web interface.
- **Merge PDFs:** The backend uses `PdfMerger` from PyPDF2 to combine the uploaded files in order.
- **Download Output:** The merged PDF is returned as a downloadable file directly from the server.

***

### ⚙️ Getting Started

Follow these steps to set up the project on your local machine:

**1. Clone the repository**

```bash
git clone https://github.com/HappyShadowCoder/FlaskPDFMerger.git
cd FlaskPDFMerger
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Run the development server**

```bash
python app.py
```

The application will be running at http://localhost:5000.

***

### 🗺️ Future Updates

Potential improvements for the project include:

**Drag-and-Drop Upload**: Allow users to drag files directly into the browser.

**Reorder Pages**: Let users rearrange PDFs before merging.

**PDF Compression**: Reduce file size of merged PDFs.

**Cloud Storage Integration**: Save merged PDFs to Google Drive or Dropbox.

***

### 📜 Version
**v1.0.0** 

Initial release with full PDF merging functionality and web interface.

**v2.0.0**  

Major Security and Reliability Update 🔒
This version introduces a robust IP address handling fix for reverse proxies and the addition of a dedicated admin check API endpoint to ensure secure and reliable access to administrative features.
