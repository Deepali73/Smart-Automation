from flask import Flask, request, jsonify
import pywhatkit as kit

app = Flask(__name__)
messages_db = []

# ========================= API ROUTES =========================

# 📥 GET: View all sent messages
@app.route("/whatsapp/messages", methods=["GET"])
def get_all_messages():
    return jsonify({"sent_messages": messages_db})


# 📤 POST: Send a WhatsApp message
@app.route("/whatsapp/send", methods=["POST"])
def send_whatsapp():
    try:
        # Get phone and message from form data or JSON
        phone = request.form.get('phone') or request.json.get('phone')
        message = request.form.get('message') or request.json.get('message')

        if not phone or not message:
            return jsonify({"error": "Both 'phone' and 'message' are required."}), 400

        # Save to local in-memory DB
        messages_db.append({"phone": phone, "message": message})

        # Send message instantly via WhatsApp
        kit.sendwhatmsg_instantly(phone_no=phone, message=message)

        return jsonify({"status": "✅ Message sent", "phone": phone, "message": message})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ========================= MAIN =========================
if __name__ == "__main__":
    app.run(debug=True)

