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





from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
download_logs = []  # List to store downloaded file logs

# Route to view download logs
@app.route("/downloads/logs", methods=["GET"])
def get_download_logs():
    return jsonify({"downloads": download_logs})

# Route to download a file from a given URL
@app.route("/downloads/file", methods=["POST"])
def download_file():
    try:
        url = request.form['url']
        filename = request.form.get('filename', 'downloaded_file.txt')

        # Get the Downloads directory
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        os.makedirs(downloads_folder, exist_ok=True)
        file_path = os.path.join(downloads_folder, filename)

        # Make the request to download the file
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                f.write(response.content)

            # Log the successful download
            download_logs.append({"url": url, "saved_as": file_path})
            return f"✅ File downloaded successfully to: {file_path}"
        else:
            return f"❌ Failed to download file. Status code: {response.status_code}"
    except Exception as e:
        return f"❌ Error occurred: {str(e)}"

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
