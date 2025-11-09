from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["GET"])
def home():
    return "Flask is running! Try visiting /check-key to test your API key."

@app.route("/check-key", methods=["GET"])
def check_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return f"✅ API Key loaded successfully: {api_key[:10]}... (hidden for safety)"
    else:
        return "❌ No API Key found. Check your .env file and restart Flask."

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.form.get("Body", "")
    sender = request.form.get("From", "")
    print(f"📩 Message from {sender}: {incoming_msg}")

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful WhatsApp assistant."},
                {"role": "user", "content": incoming_msg}
            ]
        )
        reply_text = response.choices[0].message.content.strip()

    except Exception as e:
        print("⚠️ Error:", e)
        reply_text = "Sorry, I had trouble connecting to OpenAI."

    resp = MessagingResponse()
    resp.message(reply_text)
    return str(resp)

if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(debug=debug_mode)
