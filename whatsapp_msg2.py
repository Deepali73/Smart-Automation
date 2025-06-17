------------------#FIRST-APPROACH-------------------------------
from twilio.rest import Client

def send_whatsapp_message(body, to_number, account_sid, auth_token, from_number="whatsapp:+14155238886"):
    """
    Sends a WhatsApp message using Twilio API.

    Parameters:
    - body (str): The message text.
    - to_number (str): Receiver's WhatsApp number (with country code).
    - account_sid (str): Twilio Account SID (starts with AC...).
    - auth_token (str): Twilio Auth Token.
    - from_number (str): Twilio WhatsApp-enabled number (default is sandbox number).

    Returns:
    - str: SID of the sent message if successful, else error message.
    """
    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=body,
            from_=from_number,
            to=f"whatsapp:{to_number}"
        )
        print(f"✅ Message sent! SID: {message.sid}")
        return message.sid
    except Exception as e:
        print(f"❌ Failed to send message: {e}")
        return str(e)

# ✅ Example usage
if __name__ == "__main__":
    # Replace with real Twilio credentials and verified WhatsApp number
    SID = "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # Correct format: starts with AC
    TOKEN = "your_auth_token"
    TO = "+91xxxxxxxxxx"  # Replace with your WhatsApp number
    send_whatsapp_message("Hello from Python via WhatsApp!", TO, SID, TOKEN)
