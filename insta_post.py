------------------------#FIRST-APPROACH----------------------------
from instagrapi import Client

def post_to_instagram(username: str, password: str, image_path: str, caption: str) -> str:
    try:
        cl = Client()
        cl.login(username, password)
        cl.photo_upload(image_path, caption)
        return "✅ Posted successfully!"
    except Exception as e:
        return f"❌ Error: {e}"







---------------------------#SECOND-APPROACH----------------------
from flask import Flask, request, jsonify
from instagrapi import Client

app = Flask(__name__)
post_logs = []  # Log posted content for inspection

# ========== View Instagram Post Logs ==========
@app.route("/posts/logs", methods=["GET"])
def get_post_logs():
    return jsonify({"instagram_posts": post_logs})

# ========== Post to Instagram ==========
@app.route("/posts/instagram", methods=["POST"])
def post_to_instagram_api():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        image_path = data.get("image_path")
        caption = data.get("caption")

        if not all([username, password, image_path, caption]):
            return jsonify({"error": "All fields are required: username, password, image_path, caption"}), 400

        cl = Client()
        cl.login(username, password)
        cl.photo_upload(image_path, caption)

        # Save to post logs
        post_logs.append({
            "username": username,
            "image_path": image_path,
            "caption": caption
        })

        return jsonify({"status": "✅ Instagram post uploaded successfully!"})

    except Exception as e:
        return jsonify({"error": f"❌ Error while posting to Instagram: {str(e)}"}), 500

# ========== Run Flask Server ==========
if __name__ == "__main__":
    app.run(debug=True)
