from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
email_logs = []

# ========== Core Email Sending Function ==========
def send_email(subject, body, sender_email, sender_password, receiver_email):
    try:
        # Create email structure
        message = MIMEText(body)
        message['Subject'] = subject
        message['From'] = sender_email
        message['To'] = receiver_email

        # Gmail SMTP
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()

        return "✅ Email sent successfully."
    except Exception as e:
        return f"❌ Failed to send email: {str(e)}"

# ========== API Endpoint to Send Email ==========
@app.route("/email/send", methods=["POST"])
def send_email_api():
    try:
        data = request.get_json()
        subject = data.get("subject")
        body = data.get("body")
        sender_email = data.get("sender_email")
        sender_password = data.get("sender_password")
        receiver_email = data.get("receiver_email")

        # Validate
        if not all([subject, body, sender_email, sender_password, receiver_email]):
            return jsonify({"error": "All fields are required."}), 400

        # Send the email
        result = send_email(subject, body, sender_email, sender_password, receiver_email)

        # Log it
        email_logs.append({
            "from": sender_email,
            "to": receiver_email,
            "subject": subject
        })

        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

# ========== Logs Endpoint ==========
@app.route("/email/logs", methods=["GET"])
def get_email_logs():
    return jsonify({"sent_emails": email_logs})

# ========== Run App ==========
if __name__ == "__main__":
    app.run(debug=True)
