----------------------#FIRST-APPROACH--------------------------
import smtplib
from email.mime.text import MIMEText

def send_email(subject, body, sender_email, sender_password, receiver_email):
    """
    Sends a plain text email using Gmail SMTP.

    Parameters:
    - subject (str): Email subject.
    - body (str): Email body.
    - sender_email (str): Sender's Gmail address (must be authorized).
    - sender_password (str): App-specific password for the sender email.
    - receiver_email (str): Recipient's email address.

    Returns:
    - str: Success or error message.
    """
    try:
        # Create the email content
        message = MIMEText(body)
        message['Subject'] = subject
        message['From'] = sender_email
        message['To'] = receiver_email

        # Connect and send
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()

        print("✅ Email sent successfully.")
        return "Success"
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return str(e)

# ✅ Example usage
if __name__ == "__main__":
    sender = "authorized_email@gmail.com"
    password = "your_app_password"
    receiver = "receiver@example.com"
    send_email(
        subject="Authorized Email",
        body="Hello! This is sent on your behalf.",
        sender_email=sender,
        sender_password=password,
        receiver_email=receiver
    )










---------------------#SECOND-APPROACH-------------------------
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
