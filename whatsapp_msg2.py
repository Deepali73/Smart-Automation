from flask import Flask, request, jsonify
from twilio.rest import Client

app = Flask(__name__)

# =================== WhatsApp Sender via Twilio ===================
def send_whatsapp_message(body, to_number, account_sid, auth_token, from_number="whatsapp:+14155238886"):
    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=body,
            from_=from_number,
            to=f"whatsapp:{to_number}"
        )
        return {"status": "✅ Message sent!", "sid": message.sid}
    except Exception as e:
        return {"status": "❌ Failed to send message", "error": str(e)}


# =================== API Routes ===================

@app.route("/", methods=["GET"])
def home():
    return {"message": "📲 Twilio WhatsApp Messaging API is active!"}

@app.route("/twilio/send", methods=["POST"])
def send_twilio_message():
    try:
        data = request.get_json()

        # Required fields
        body = data.get("body")
        to = data.get("to")
        sid = data.get("account_sid")
        token = data.get("auth_token")

        if not all([body, to, sid, token]):
            return jsonify({
                "error": "Missing one or more required parameters: 'body', 'to', 'account_sid', 'auth_token'"
            }), 400

        result = send_whatsapp_message(body, to, sid, token)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =================== Start Server ===================
if __name__ == "__main__":
    app.run(debug=True)
