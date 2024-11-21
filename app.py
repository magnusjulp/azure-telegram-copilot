from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
COPILOT_API_URL = os.getenv("COPILOT_API_URL")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    chat_id = data.get("message", {}).get("chat", {}).get("id")
    user_message = data.get("message", {}).get("text", "")

    # Forward message to CoPilot API
    copilot_response = requests.post(COPILOT_API_URL, json={"query": user_message})
    copilot_text = copilot_response.json().get("response", "I'm not sure how to answer that.")

    # Send response to Telegram
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(telegram_url, json={"chat_id": chat_id, "text": copilot_text})

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
