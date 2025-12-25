from flask import Flask, request
from database import payments, users
from config import ADMIN_PANEL_PASSWORD

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def panel():
    if request.args.get("pass") != ADMIN_PANEL_PASSWORD:
        return "Unauthorized"

    html = "<h2>PKdlg_bot Admin Panel</h2>"
    html += "<h3>Pending Payments</h3>"

    for p in payments.find({"status": "pending"}):
        html += f"""
        <p>User: {p['uid']} | Trx: {p['trx']}
        → /approve {p['trx']} DAYS</p>
        """

    html += "<h3>Users</h3>"
    html += f"<p>Total Users: {users.count_documents({})}</p>"
    return html