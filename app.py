from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").lower()
    response = MessagingResponse()
    response.message(f"Hey! You said: {incoming_msg}")
    return str(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
