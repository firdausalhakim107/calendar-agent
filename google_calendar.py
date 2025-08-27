import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Build paths relative to this script's directory
script_dir = os.path.dirname(__file__)
TOKEN_PATH = os.path.join(script_dir, "token.json")
CREDS_PATH = os.path.join(script_dir, "credentials.json")


def get_calendar_service():
    """
    Authenticates with the Google Calendar API and returns a service object.
    It handles the OAuth 2.0 flow and token storage.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # The credentials.json file is required for the OAuth 2.0 flow.
            # It should be placed in the same directory as this script.
            if not os.path.exists(CREDS_PATH):
                raise FileNotFoundError(f"'{CREDS_PATH}' not found. Please place your Google API credentials in this file.")

            flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)
        return service
    except HttpError as error:
        print(f"An error occurred while building the service: {error}")
        return None


def create_event(service, summary, start_time, end_time):
    """
    Creates an event in the user's primary calendar.

    Args:
        service: The authenticated Google Calendar service object.
        summary: The summary or title of the event.
        start_time: The start time of the event.
        end_time: The end time of the event.

    Returns:
        The created event object, or None if an error occurred.
    """
    event = {
        "summary": summary,
        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": "UTC",
        },
        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": "UTC",
        },
    }

    try:
        event = (
            service.events()
            .insert(calendarId="primary", body=event)
            .execute()
        )
        print(f"Event created: {event.get('htmlLink')}")
        return event
    except HttpError as error:
        print(f"An error occurred while creating the event: {error}")
        return None

if __name__ == "__main__":
    # Example of how to use the functions in this file.
    # This will not be executed when the file is imported.
    service = get_calendar_service()
    if service:
        # Create an event for tomorrow at 10am for 1 hour.
        now = datetime.datetime.utcnow()
        start_time = now + datetime.timedelta(days=1)
        start_time = start_time.replace(hour=10, minute=0, second=0, microsecond=0)
        end_time = start_time + datetime.timedelta(hours=1)
        create_event(service, "Example Event from google_calendar.py", start_time, end_time)
