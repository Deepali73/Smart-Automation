from twilio.rest import Client

def send_sms_twilio(account_sid: str, auth_token: str, from_number: str, to_number: str, message_body: str):
    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=message_body,
            from_=from_number,
            to=to_number
        )
        print(f"Message sent successfully! SID: {message.sid}")
    except Exception as e:
        print("Error sending message:", e)




from flask import Flask, request
from twilio.rest import Client

app = Flask(__name__)
sms_logs = []  # In-memory log of sent messages

# Route to view sent SMS logs
@app.route("/sms/logs", methods=["GET"])
def get_sms_logs():
    return {"sms_sent": sms_logs}

# Route to send an SMS using Twilio
@app.route("/sms/send", methods=["POST"])
def send_sms_api():
    try:
        # Get form data
        account_sid = request.form['account_sid']
        auth_token = request.form['auth_token']
        from_phone = request.form['from']
        to_phone = request.form['to']
        message = request.form['message']

        # Store in logs
        sms_logs.append({
            "from": from_phone,
            "to": to_phone,
            "message": message
        })

        # Call SMS function
        send_sms_twilio(account_sid, auth_token, from_phone, to_phone, message)
        return f"✅ SMS sent to {to_phone} from {from_phone}"

    except Exception as e:
        return f"❌ Failed to send SMS: {str(e)}"

# Twilio SMS sending function
def send_sms_twilio(account_sid: str, auth_token: str, from_number: str, to_number: str, message_body: str):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message_body,
        from_=from_number,
        to=to_number
    )
    print(f"SMS sent! SID: {message.sid}")

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
