from instagrapi import Client

def post_to_instagram(username: str, password: str, image_path: str, caption: str) -> str:
    try:
        cl = Client()
        cl.login(username, password)
        cl.photo_upload(image_path, caption)
        return "✅ Posted successfully!"
    except Exception as e:
        return f"❌ Error: {e}"
