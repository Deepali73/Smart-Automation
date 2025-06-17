----------------------#FIRST-APPROACH---------------------------
import messagebird

#create instance of messagebird.Client using API key
client = messagebird.Client('<your-api-key>')

try:
    msg = client.voice_message_create('+91xxxxxxxxxx', 'Hey you, a little bird told me you wanted a call!', { 'voice' : 'female' })
    print(msg.__dict__)

except messagebird.client.ErrorException as e:
    for error in e.errors:
        print(error)







---------------------------#SECOND-APPROACH-----------------------------
from flask import Flask, request, jsonify
import messagebird

app = Flask(__name__)
call_logs = []  # In-memory list to store call logs

# =====================================
# GET /calls/logs
# View all voice call logs
# =====================================
@app.route("/calls/logs", methods=["GET"])
def get_call_logs():
    return jsonify({"voice_calls": call_logs})

# =====================================
# POST /calls/make
# Trigger a voice call via MessageBird
# =====================================
@app.route("/calls/make", methods=["POST"])
def make_voice_call():
    try:
        api_key = request.form.get('api_key')
        recipient = request.form.get('recipient')
        voice_message = request.form.get('message')
        voice_gender = request.form.get('voice', 'female')  # Default to female

        if not all([api_key, recipient, voice_message]):
            return jsonify({"error": "Missing required parameters."}), 400

        # Create client
        client = messagebird.Client(api_key)

        # Send voice call
        msg = client.voice_message_create(
            recipient,
            voice_message,
            {"voice": voice_gender}
        )

        # Log the call
        call_logs.append({
            "recipient": recipient,
            "message": voice_message,
            "voice": voice_gender,
            "message_id": msg.id
        })

        return jsonify({
            "status": "✅ Voice call placed",
            "recipient": recipient,
            "message_id": msg.id
        })

    except messagebird.client.ErrorException as e:
        error_msgs = [err.description for err in e.errors]
        return jsonify({"status": "❌ Failed", "errors": error_msgs}), 500

    except Exception as e:
        return jsonify({"status": "❌ Unexpected error", "details": str(e)}), 500

# =====================================
# Run the Flask app
# =====================================
if __name__ == "__main__":
    app.run(debug=True)
