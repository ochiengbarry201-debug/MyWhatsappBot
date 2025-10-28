from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Get API keys securely
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the route Twilio will call
@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    # Get the incoming message text
    incoming_msg = request.values.get("Body", "").strip()
    
    # Initialize Twilio response object
    resp = MessagingResponse()
    msg = resp.message()

    # If a message is received
    if incoming_msg:
        try:
            # Send user's message to ChatGPT
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": incoming_msg}]
            )
            
            # Extract reply text
            reply = completion.choices[0].message["content"].strip()
            
            # Send reply back to user on WhatsApp
            msg.body(reply)
        
        except Exception as e:
            msg.body("⚠️ Oops! Something went wrong: " + str(e))
    else:
        msg.body("👋 Hey there! Send me a message to start chatting!")

    return str(resp)

# Run the Flask server locally (Render will handle it in deployment)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

