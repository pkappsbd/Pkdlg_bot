import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")

MONGO_URI = os.getenv("MONGO_URI")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
FORCE_SUB_CHANNEL = os.getenv("FORCE_SUB_CHANNEL")

SHORTENER_API_KEY = os.getenv("SHORTENER_API_KEY")
SHORTENER_BASE_URL = os.getenv("SHORTENER_BASE_URL")

ADMIN_PANEL_PASSWORD = os.getenv("ADMIN_PANEL_PASSWORD")