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