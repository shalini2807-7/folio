# Pulse - Daily Summary Bot
# Fetches: weather (wttr.in) + a quote (zenquotes.io)
# Runs:    every day at 8 AM IST via GitHub Actions

import requests
from datetime import date

def get_weather(city="Thiruvananthapuram"):
    """Fetch today's weather as a one-line text summary."""
    url = f"https://wttr.in/{city}?format=3"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text.strip()  # remove trailing newline
    except Exception as e:
        return f"Weather unavailable ({e})"
    
def get_quote():
    """Fetch a random motivational quote from ZenQuotes."""
    url = "https://zenquotes.io/api/random"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()  # JSON -> Python list
        quote = data[0]["q"]
        author = data[0]["a"]
        return f'"{quote}" — {author}'
    except Exception as e:
        return f"Quote unavailable ({e})"
    
def build_summary():
    """Assemble the full daily summary from all data sources."""
    today = date.today().strftime("%A, %d %b %Y")
    weather = get_weather()
    quote = get_quote()

    summary = f"""
========================================
PULSE - Daily Summary
{today}
========================================

WEATHER
{weather}

TODAY'S QUOTE
{quote}
========================================
"""
    return summary

def run():
    """Main entry point. Called by GitHub Actions."""
    summary = build_summary()
    print(summary)  # shows in the Actions log

    # Save to a file (uploaded as a downloadable artifact)
    with open("daily_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)
    print("Pulse ran successfully.")

if __name__ == "__main__":
    run()

import os

import os
import smtplib
from email.mime.text import MIMEText

def send_email(summary_text):
    # Pull credentials securely from the background environment mapping
    sender = os.environ.get("EMAIL_SENDER")
    password = os.environ.get("EMAIL_PASSWORD")
    receiver = os.environ.get("EMAIL_RECEIVER")

    # If any environmental variables are missing, exit gracefully
    if not sender or not password or not receiver:
        print("Email credentials missing. Skipping email delivery step.")
        return

    # Construct the message container structure
    msg = MIMEText(summary_text)
    msg["Subject"] = "Pulse - Daily Summary"
    msg["From"] = sender
    msg["To"] = receiver

    try:
        # Establish a secure connection tunnel to Gmail's mail server
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
        print("Email sent.")
    except Exception as e:
        print(f"Failed to deliver email: {e}")
# Grabs it dynamically; no secret strings are ever saved in this file!
api_key = os.environ.get("WEATHER_API_KEY")