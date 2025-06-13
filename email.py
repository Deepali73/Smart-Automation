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




from flask import Flask, request
import smtplib

app = Flask(__name__)
email_log = []  # In-memory "database"

# Route to view all email logs
@app.route("/email/logs", methods=["GET"])
def get_email_logs():
    return {"emails_sent": email_log}

# Route to send email
@app.route("/email/send", methods=["POST"])
def send_email_api():
    try:
        sender = request.form['sender']
        receiver = request.form['receiver']
        app_password = request.form['password']
        message = request.form['message']

        # Store log
        email_log.append({
            "from": sender,
            "to": receiver,
            "message": message
        })

        # Send email
        send_email(sender, receiver, app_password, message)

        return f"✅ Email successfully sent from {sender} to {receiver}!"

    except Exception as e:
        return f"❌ Failed to send email: {str(e)}"

# Function to send email using Gmail SMTP
def send_email(sender_email: str, receiver_email: str, app_password: str, message: str):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, message)
        print("Email sent successfully!")
    finally:
        server.quit()

# Run the Flask server
if __name__ == "__main__":
    app.run(debug=True)
