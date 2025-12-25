from flask import Flask
from threading import Thread
from admin_panel import app as admin_app

app = Flask(__name__)

@app.route("/")
def home():
    return "PKdlg_bot running 🚀"

def run():
    admin_app.run(host="0.0.0.0", port=8080)

def keep_alive():
    Thread(target=run).start()