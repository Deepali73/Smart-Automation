-----------------------#FIRST-APPROACH----------------------
import smtplib

def send_email(sender_email: str, receiver_email: str, app_password: str, message: str):
    try:
        # create SMTP session
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # secure the connection

        # login with app password
        server.login(sender_email, app_password)

        # send the email
        server.sendmail(sender_email, receiver_email, message)
        print("Email sent successfully!")

    except Exception as e:
        print("Error:", e)

    finally:
        server.quit()







------------------------#SECOND-APPROACH-------------------------------
from flask import Flask, request, jsonify
import smtplib

app = Flask(__name__)
email_log = []  # In-memory log of sent emails

# ========================
# Send Email Using Gmail
# ========================
def send_email(sender_email: str, receiver_email: str, app_password: str, message: str):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, message)
        print("✅ Email sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return str(e)
    finally:
        server.quit()

# ===========================
# API: Send Email (POST)
# ===========================
@app.route("/email/send", methods=["POST"])
def send_email_api():
    try:
        sender = request.form.get('sender')
        receiver = request.form.get('receiver')
        app_password = request.form.get('password')
        message = request.form.get('message')

        # Basic validation
        if not all([sender, receiver, app_password, message]):
            return jsonify({"error": "All fields are required (sender, receiver, password, message)."}), 400

        # Call sending function
        result = send_email(sender, receiver, app_password, message)

        # Log the activity
        email_log.append({
            "from": sender,
            "to": receiver,
            "message": message
        })

        if result is True:
            return jsonify({"status": "✅ Email successfully sent!", "from": sender, "to": receiver})
        else:
            return jsonify({"status": "❌ Failed to send email", "error": result}), 500

    except Exception as e:
        return jsonify({"status": "❌ Error", "details": str(e)}), 500

# ============================
# API: Email Logs (GET)
# ============================
@app.route("/email/logs", methods=["GET"])
def get_email_logs():
    return jsonify({"emails_sent": email_log})

# ============================
# Run Server
# ============================
if __name__ == "__main__":
    app.run(debug=True)
