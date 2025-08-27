# WhatsApp Google Calendar Agent

This project is a Python-based agent that connects to Google Calendar and allows you to manage your calendar events through WhatsApp messages. You can create new events by sending a message to a designated WhatsApp number.

## Features

-   Create Google Calendar events using natural language from WhatsApp.
-   Receive confirmations for created events.
-   Easy to set up and configure.

## Setup

### 1. Clone the repository

```bash
git clone <repository_url>
cd calendar-agent
```

### 2. Install dependencies

Install the required Python libraries using pip:

```bash
pip install -r requirements.txt
```

### 3. Configure Google Calendar API

To use this agent, you need to enable the Google Calendar API and get credentials.

1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a new project.
3.  Enable the "Google Calendar API" for your project.
4.  Create credentials for a "Desktop application".
5.  Download the `credentials.json` file and place it in the root directory of this project.

When you first run the application, you will be prompted to authorize access to your Google Calendar. Follow the on-screen instructions to complete the authorization process. A `token.json` file will be created to store your access tokens for future use.

### 4. Configure Twilio for WhatsApp

This agent uses [Twilio](https://www.twilio.com/) to send and receive WhatsApp messages.

1.  Create a Twilio account if you don't have one.
2.  Get a Twilio phone number that is WhatsApp-enabled.
3.  Find your "Account SID" and "Auth Token" from your Twilio dashboard.
4.  Set up the Twilio Sandbox for WhatsApp or request production access for your number.
5.  Configure the webhook for incoming messages to point to your server's URL (e.g., `https://<your-server-address>/whatsapp`). You will need to deploy this application on a server with a public IP or use a tool like [ngrok](https://ngrok.com/) for local development.

### 5. Configure Environment Variables

This project uses a `.env` file to manage secret keys and configuration.

1.  In the root directory of the project, make a copy of the `.env.example` file and name it `.env`.

    ```bash
    cp .env.example .env
    ```

2.  Open the `.env` file and add your Twilio credentials. You can find these in your [Twilio Console](https://www.twilio.com/console).

    ```
    # .env

    TWILIO_ACCOUNT_SID="your_twilio_account_sid"
    TWILIO_AUTH_TOKEN="your_twilio_auth_token"
    TWILIO_WHATSAPP_NUMBER="whatsapp:+14155238886" # Or your own Twilio WhatsApp number
    ```

## Usage

1.  **Run the application:**

    ```bash
    python main.py
    ```

2.  **Send a message to your WhatsApp number:**

    Send a message in a natural format to create an event. For example:

    `"Schedule a meeting with John tomorrow at 10am"`

    The agent will parse the message and create an event in your Google Calendar. You will receive a confirmation message on WhatsApp.

    Supported commands:
    -   Currently, the agent supports creating events with a title, date, and time.
