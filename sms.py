from flask import Flask, request, jsonify
from twilio.rest import Client

app = Flask(__name__)
sms_logs = []  # In-memory list to track sent SMS

# ========== Twilio SMS Sending Function ==========
def send_sms_twilio(account_sid: str, auth_token: str, from_number: str, to_number: str, message_body: str):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message_body,
        from_=from_number,
        to=to_number
    )
    return message.sid

# ========== View Sent SMS Logs ==========
@app.route("/sms/logs", methods=["GET"])
def get_sms_logs():
    return jsonify({"sms_sent": sms_logs})

# ========== Send SMS ==========
@app.route("/sms/send", methods=["POST"])
def send_sms_api():
    try:
        data = request.get_json()

        # Required parameters
        account_sid = data.get("account_sid")
        auth_token = data.get("auth_token")
        from_phone = data.get("from")
        to_phone = data.get("to")
        message = data.get("message")

        if not all([account_sid, auth_token, from_phone, to_phone, message]):
            return jsonify({"error": "Missing one or more required parameters."}), 400

        # Store in log
        sms_logs.append({
            "from": from_phone,
            "to": to_phone,
            "message": message
        })

        sid = send_sms_twilio(account_sid, auth_token, from_phone, to_phone, message)
        return jsonify({
            "status": "✅ SMS sent successfully.",
            "sid": sid,
            "to": to_phone
        })

    except Exception as e:
        return jsonify({"error": f"❌ Failed to send SMS: {str(e)}"}), 500

# ========== Run App ==========
if __name__ == "__main__":
    app.run(debug=True)
