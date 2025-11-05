from flask import Flask, request, jsonify, send_file
import os, requests, zipfile
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tempfile import mkdtemp

app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 Web Clone API Running!"

@app.route('/clone', methods=['POST'])
def clone_site():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'Missing URL'}), 400

    temp_dir = mkdtemp()
    html_file = os.path.join(temp_dir, "index.html")

    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        # Save HTML file
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(str(soup))

        # ZIP file path
        zip_path = os.path.join(temp_dir, "site.zip")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            z.write(html_file, "index.html")

        return send_file(zip_path, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
