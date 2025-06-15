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
