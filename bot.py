# Pulse - Daily Summary Bot
# Fetches: OpenWeatherMap (Task 1) + a quote (zenquotes.io)
# Runs:    every day at 8 AM IST via GitHub Actions

import os
import requests
import smtplib
from datetime import date
from email.mime.text import MIMEText

def get_weather_and_check_alerts(city="Thiruvananthapuram"):
    """Fetch weather from OpenWeatherMap and determine if an alert is needed."""
    # Pull the OpenWeather API key securely from environment variables
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    
    # If no API key is provided, gracefully fallback to the old free wttr.in format
    if not api_key:
        print("OPENWEATHER_API_KEY missing. Falling back to wttr.in...")
        try:
            url = f"https://wttr.in/{city}?format=3"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text.strip(), False, ""
        except Exception as e:
            return f"Weather unavailable ({e})", False, ""

    # OpenWeatherMap API implementation
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=10).json()
        
        # Extract temperature and description fields
        temp = response["main"]["temp"]
        weather_desc = response["weather"][0]["description"].lower()
        main_weather = response["weather"][0]["main"].lower()
        
        weather_summary = f"{city}: {temp}°C, {weather_desc.capitalize()}"
        
        # Task 1 Conditions: Temp > 35°C OR Rain predicted
        is_too_hot = temp > 35
        is_raining = "rain" in weather_desc or "rain" in main_weather
        
        alert_content = ""
        trigger_alert = False
        
        if is_too_hot or is_raining:
            trigger_alert = True
            alert_content = f"⚠️ WEATHER ALERT FOR {city.upper()} ⚠️\n\n"
            if is_too_hot:
                alert_content += f"• Extreme Heat Warning: Temperature is currently {temp}°C!\n"
            if is_raining:
                alert_content += f"• Rain Warning: Precipitation detected ({weather_desc}).\n"
            alert_content += "\nTake necessary precautions!"
            
        return weather_summary, trigger_alert, alert_content

    except Exception as e:
        return f"OpenWeatherMap unavailable ({e})", False, ""
    
def get_quote():
    """Fetch a random motivational quote from ZenQuotes."""
    url = "https://zenquotes.io/api/random"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        quote = data[0]["q"]
        author = data[0]["a"]
        return f'"{quote}" — {author}'
    except Exception as e:
        return f"Quote unavailable ({e})"

def send_email(subject, content):
    """Securely email the alert or summary using Gmail SMTP."""
    sender = os.environ.get("EMAIL_SENDER")
    password = os.environ.get("EMAIL_PASSWORD")
    receiver = os.environ.get("EMAIL_RECEIVER")

    if not sender or not password or not receiver:
        print("Email credentials missing. Skipping email delivery step.")
        return

    msg = MIMEText(content)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
        print(f"Email sent successfully: '{subject}'")
    except Exception as e:
        print(f"Failed to deliver email: {e}")

def run():
    """Main entry point. Called by GitHub Actions."""
    print("Running Pulse Core Pipeline...")
    today = date.today().strftime("%A, %d %b %Y")
    
    # 1. Fetch weather and evaluate if Task 1 alert parameters match
    weather, trigger_alert, alert_text = get_weather_and_check_alerts()
    quote = get_quote()

    # 2. Compile the local logging dashboard report text
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
    print(summary)

    # 3. Save snapshot summary text artifact
    with open("daily_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)
    print("Artifact saved to daily_summary.txt")

    # 4. Handle Task 1 Automated Email Alerts conditional check
    if trigger_alert:
        print("Task 1 Alert triggered! Preparing email dispatch...")
        send_email("🚨 Pulse Weather Alert!", alert_text)
    else:
        print("Weather parameters normal. No email alert sent today.")

if __name__ == "__main__":
    run()