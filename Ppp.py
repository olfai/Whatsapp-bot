from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ---------------------------
# Your Credentials
# ---------------------------
VERIFY_TOKEN = "ABC123XYZ"
WHATSAPP_TOKEN = "EAANjdQDk2foBRQyLh0Kx7AolhinBOCAEDMUpVLovvuRN1ItyWNPMoePOwdLf1KFSHmSlJBNheWYHAgt2d6R0vaMB4qPcl1MO3Fyt0ZBAqwcY7Pc1cEo2uG4vZC44d2v0D9ivVUZBYl4F006VS4PVELZAiHSMWM6y2ps8KAQddubdpGWqGCwp7ZCdjZAQZA3"
PHONE_NUMBER_ID = "1076019785602618"

# ---------------------------
# Send WhatsApp Message
# ---------------------------
def send_message(number, message):
    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": number,
        "text": {"body": message}
    }
    requests.post(url, json=data, headers=headers)

# ---------------------------
# Keyword Replies
# ---------------------------
KEYWORD_REPLIES = {
    "hi": "Hello! How can I help you?",
    "hello": "Hello! How can I assist you today?",

    "price": "Our pricing starts at ₹499. Want more details?",
    "pricing": "Our pricing starts at ₹499. Want more details?",

    "services": "We offer automation, WhatsApp bots, and marketing services.",

    "help": "Commands: hi, price, services, location, brochure",

    "location": "Here is our location: https://maps.google.com/",

    "brochure": "Sending brochure soon."
}

# ---------------------------
# Verify Webhook (GET)
# ---------------------------
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403

# ---------------------------
# Incoming Message Handler (POST)
# ---------------------------
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        number = message["from"]
        user_text = message.get("text", {}).get("body", "").lower()

        # Detect reply
        reply = KEYWORD_REPLIES.get(user_text, "Sorry, I didn't understand. Type *help*.")

        # Log to console (Render logs)
        print(f"User said: {user_text}")
        print(f"Bot replied: {reply}")

        # Send WhatsApp message
        send_message(number, reply)

    except Exception as e:
        print("Error:", e)

    return jsonify(success=True)

# ---------------------------
# Run Local
# ---------------------------
if __name__ == "__main__":
    app.run(port=5000)
