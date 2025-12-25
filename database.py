from pymongo import MongoClient
from datetime import datetime, timedelta
from config import MONGO_URI

db = MongoClient(MONGO_URI)["PKdlg_bot"]

users = db.users
files = db.files
payments = db.payments


def add_user(uid, ref=None):
    if not users.find_one({"_id": uid}):
        users.insert_one({
            "_id": uid,
            "premium": False,
            "expiry": None,
            "ref": ref,
            "balance": 0,
            "joined": datetime.utcnow()
        })


def is_premium(uid):
    u = users.find_one({"_id": uid})
    if not u or not u["premium"]:
        return False
    if u["expiry"] and u["expiry"] < datetime.utcnow():
        users.update_one({"_id": uid}, {"$set": {"premium": False}})
        return False
    return True


def add_premium(uid, days):
    users.update_one(
        {"_id": uid},
        {"$set": {
            "premium": True,
            "expiry": datetime.utcnow() + timedelta(days=days)
        }}
    )


def save_file(fid, token, hours=24):
    files.insert_one({
        "fid": fid,
        "token": token,
        "expires": datetime.utcnow() + timedelta(hours=hours)
    })


def get_file(token):
    f = files.find_one({"token": token})
    if not f or f["expires"] < datetime.utcnow():
        return None
    return f


def add_payment(uid, trx):
    payments.insert_one({
        "uid": uid,
        "trx": trx,
        "status": "pending",
        "time": datetime.utcnow()
    })


def approve_payment(trx, days):
    p = payments.find_one({"trx": trx, "status": "pending"})
    if not p:
        return False
    add_premium(p["uid"], days)
    payments.update_one({"trx": trx}, {"$set": {"status": "approved"}})
    if users.find_one({"_id": p["uid"]}).get("ref"):
        users.update_one(
            {"_id": users.find_one({"_id": p["uid"]})["ref"]},
            {"$inc": {"balance": 10}}
        )
    return True