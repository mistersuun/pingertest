import os
import requests
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# The URL to ping
TARGET_URL = "https://5b313c06-e426-4a40-85a0-374d8b30247e-00-l237zun9iliw.kirk.replit.dev/"

def ping_target():
    try:
        response = requests.get(TARGET_URL, timeout=10)
        logger.info("Pinged %s, status code: %s", TARGET_URL, response.status_code)
    except Exception as e:
        logger.error("Error pinging %s: %s", TARGET_URL, e)

# Set up the scheduler to run the ping_target function every 20 minutes.
scheduler = BackgroundScheduler()
scheduler.add_job(func=ping_target, trigger="interval", minutes=3)
scheduler.start()

@app.route("/")
def index():
    return "Pinger is running!"

if __name__ == "__main__":
    # Use the PORT environment variable if available (Heroku sets this)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
