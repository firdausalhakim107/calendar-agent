from twilio.rest import Client
import config

# Initialize Twilio client.
# This will fail if the configuration is not set up, which is handled gracefully.
try:
    if config.TWILIO_ACCOUNT_SID:
        client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
    else:
        client = None
except Exception as e:
    print(f"Could not initialize Twilio client: {e}")
    client = None

def send_message(to, body):
    """
    Sends a WhatsApp message using Twilio.

    Args:
        to: The recipient's WhatsApp number.
        body: The message to send.
    """
    if not client:
        print("Twilio client not initialized. Cannot send message.")
        return

    try:
        message = client.messages.create(
            from_=config.TWILIO_WHATSAPP_NUMBER,
            body=body,
            to=to
        )
        print(f"Message sent to {to}: {message.sid}")
    except Exception as e:
        print(f"Error sending message to {to}: {e}")
