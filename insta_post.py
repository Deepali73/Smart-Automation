from instagrapi import Client

def post_to_instagram(username: str, password: str, image_path: str, caption: str) -> str:
    try:
        cl = Client()
        cl.login(username, password)
        cl.photo_upload(image_path, caption)
        return "✅ Posted successfully!"
    except Exception as e:
        return f"❌ Error: {e}"




from flask import Flask, request, jsonify
from instagrapi import Client

app = Flask(__name__)
post_logs = []  # For storing logs of posted content

# Route to log and retrieve post attempts
@app.route("/posts/logs", methods=["GET"])
def get_post_logs():
    return jsonify({"instagram_posts": post_logs})

# Route to post a photo to Instagram
@app.route("/posts/instagram", methods=["POST"])
def post_to_instagram_api():
    try:
        username = request.form['username']
        password = request.form['password']
        image_path = request.form['image_path']
        caption = request.form['caption']

        cl = Client()
        cl.login(username, password)
        cl.photo_upload(image_path, caption)

        # Save to logs
        post_logs.append({
            "username": username,
            "image_path": image_path,
            "caption": caption
        })

        return "✅ Instagram post uploaded successfully!"
    except Exception as e:
        return f"❌ Error while posting to Instagram: {str(e)}"

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
