from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
from datetime import timedelta
import dateparser

import google_calendar

app = Flask(__name__)

# Get Google Calendar service.
# This will trigger the authentication flow on the first run.
# Make sure you have your `credentials.json` file in the root directory.
try:
    calendar_service = google_calendar.get_calendar_service()
except FileNotFoundError:
    print("\nERROR: `credentials.json` not found.")
    print("Please follow the instructions in the README.md to set up Google Calendar API credentials.\n")
    calendar_service = None

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    """
    Handles incoming WhatsApp messages from Twilio.
    It parses the message for a date and time, creates a Google Calendar event,
    and sends a confirmation back to the user.
    """
    if not calendar_service:
        response = MessagingResponse()
        response.message("The Calendar Agent is not configured correctly. Missing Google Calendar credentials.")
        return Response(str(response), mimetype="application/xml")

    incoming_msg = request.values.get("Body", "").strip()
    from_number = request.values.get("From", "")

    print(f"Received message '{incoming_msg}' from {from_number}")

    # Use dateparser to find the date and time in the message.
    # 'PREFER_DATES_FROM': 'future' helps resolve ambiguities like "tomorrow".
    parsed_time = dateparser.parse(incoming_msg, settings={'PREFER_DATES_FROM': 'future'})

    response = MessagingResponse()

    if not parsed_time:
        response_msg = "I couldn't understand the date and time in your message. Please try again with a clearer time (e.g., 'Meeting with team tomorrow at 3pm' or 'Dentist appointment next Tuesday at 10am')."
        response.message(response_msg)
    else:
        # Assume the event is 1 hour long by default.
        end_time = parsed_time + timedelta(hours=1)

        # Create the event on Google Calendar.
        event = google_calendar.create_event(
            calendar_service,
            summary=incoming_msg,
            start_time=parsed_time,
            end_time=end_time
        )

        if event:
            event_summary = event.get('summary')
            start = event.get('start', {}).get('dateTime', '')

            # Format the date for readability.
            try:
                start_dt = dateparser.parse(start)
                # Format to "Monday, January 01 at 12:00 PM"
                formatted_start = start_dt.strftime('%A, %B %d at %I:%M %p')
                response_msg = f"🗓️ Event created!\n\n'{event_summary}' is scheduled for {formatted_start}."
            except Exception:
                response_msg = f"🗓️ Event created! '{event_summary}'"

            response.message(response_msg)
        else:
            response_msg = "Sorry, I encountered an error and couldn't create the event in your calendar. Please try again."
            response.message(response_msg)

    return Response(str(response), mimetype="application/xml")


if __name__ == "__main__":
    # When running locally, use a tool like ngrok to expose this port to the internet
    # and set the webhook URL in your Twilio console.
    # Example: ngrok http 5000
    print("Starting Flask server...")
    print("Make sure your Twilio webhook is pointing to http://<your-ngrok-url>/whatsapp")
    app.run(host="0.0.0.0", port=5000, debug=True)
