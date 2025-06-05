from twilio.rest import Client

# Your Twilio account credentials
account_sid = 'ACCOUNT_SID'
auth_token = 'AUTH_TOKEN'
client = Client(account_sid, auth_token)

# Send the message
message = client.messages.create(
    body="Hello from Python!",
    from_='+91xxxxxxxxxx',  # Your Twilio phone number with country code
    to='+91xxxxxxxxxx'      # Destination phone number with country code
)

print(f"Message sent, SID: {message.sid}")
