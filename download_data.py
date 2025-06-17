----------------------------#FIRST-APPROACH-------------------------
import requests
import os

# URL of the file you want to download
url = "https://www.google.com"

# Get the user's Downloads directory
downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
file_name = os.path.join(downloads_folder, "sample-file.txt")

# Download the file
response = requests.get(url)

if response.status_code == 200:
    with open(file_name, "wb") as file:
        file.write(response.content)
    print(f"File downloaded successfully to {file_name}")
else:
    print("Failed to download file.")







---------------------------#SECOND-APPROACH------------------------------
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
download_logs = []  # In-memory list to store download logs

# ===========================
# API: View Download Logs
# ===========================
@app.route("/downloads/logs", methods=["GET"])
def get_download_logs():
    return jsonify({"downloads": download_logs})

# ===========================
# API: Download File (POST)
# ===========================
@app.route("/downloads/file", methods=["POST"])
def download_file():
    try:
        url = request.form.get('url')
        filename = request.form.get('filename', 'downloaded_file.txt')

        if not url:
            return jsonify({"error": "Missing 'url' parameter."}), 400

        # Destination folder: ~/Downloads
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        os.makedirs(downloads_folder, exist_ok=True)
        file_path = os.path.join(downloads_folder, filename)

        # Make the download request
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                f.write(response.content)

            # Log the download
            download_logs.append({
                "url": url,
                "filename": filename,
                "saved_path": file_path
            })

            return jsonify({
                "status": "✅ File downloaded successfully!",
                "saved_path": file_path
            })
        else:
            return jsonify({
                "status": "❌ Download failed",
                "http_status": response.status_code,
                "url": url
            }), response.status_code

    except Exception as e:
        return jsonify({"status": "❌ Error occurred", "details": str(e)}), 500

# ===========================
# Run Flask Server
# ===========================
if __name__ == "__main__":
    app.run(debug=True)
