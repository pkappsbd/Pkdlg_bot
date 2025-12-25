# server.py
from flask import Flask
from threading import Thread
from admin_panel import app as admin_app  # তোমার admin_panel.py থেকে Flask app
from main import start_bot  # main.py এর Bot start function (Pyrogram Client)

# Flask main app for UptimeRobot ping
app = Flask(__name__)

@app.route("/")
def home():
    return "PKdlg_bot running 🚀"

# Function to run admin panel in a separate thread
def run_admin_panel():
    admin_app.run(host="0.0.0.0", port=8080)

# Function to keep admin panel alive
def keep_alive():
    Thread(target=run_admin_panel).start()

# Main entry
if __name__ == "__main__":
    # Start admin panel in background
    keep_alive()
    
    # Start your Telegram bot
    start_bot()  # main.py এর function যা bot.run() করে