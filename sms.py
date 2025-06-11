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
