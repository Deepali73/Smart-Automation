import messagebird

#create instance of messagebird.Client using API key
client = messagebird.Client('<your-api-key>')

try:
    msg = client.voice_message_create('+91xxxxxxxxxx', 'Hey you, a little bird told me you wanted a call!', { 'voice' : 'female' })
    print(msg.__dict__)

except messagebird.client.ErrorException as e:
    for error in e.errors:
        print(error)





from flask import Flask, request
import messagebird

app = Flask(__name__)
call_logs = []  # Stores voice call request logs

# Route to view voice call logs
@app.route("/calls/logs", methods=["GET"])
def get_call_logs():
    return {"voice_calls": call_logs}

# Route to trigger a voice call
@app.route("/calls/make", methods=["POST"])
def make_voice_call():
    try:
        # Get request form data
        api_key = request.form['api_key']
        recipient = request.form['recipient']
        voice_message = request.form['message']
        voice_gender = request.form.get('voice', 'female')  # Default: female

        # Log the request
        call_logs.append({
            "to": recipient,
            "message": voice_message,
            "voice": voice_gender
        })

        # Create voice call
        client = messagebird.Client(api_key)
        msg = client.voice_message_create(recipient, voice_message, {'voice': voice_gender})

        return f"✅ Voice call placed to {recipient}. Call ID: {msg.id}"

    except messagebird.client.ErrorException as e:
        errors = "\n".join([f"❌ {err.description}" for err in e.errors])
        return f"Failed to place voice call:\n{errors}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
