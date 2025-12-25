import secrets, requests
from pyrogram import Client, filters
from config import *
from database import *
from server import keep_alive

bot = Client("PKdlg_bot", API_ID, API_HASH, BOT_TOKEN)

@bot.on_message(filters.command("start"))
async def start(c, m):
    ref = int(m.text.split()[1]) if len(m.text.split()) > 1 and m.text.split()[1].isdigit() else None
    add_user(m.from_user.id, ref)
    await m.reply(
        "🚀 **PKdlg_bot**\n\n"
        "📦 File → Permanent Link\n"
        "🔐 Free = Ads | Premium = Direct\n\n"
        f"👥 Referral ID: `{m.from_user.id}`"
    )


@bot.on_message(filters.forwarded & filters.private)
async def store(c, m):
    token = secrets.token_urlsafe(8)
    save_file(m.forward_from_message_id, token, hours=24)
    link = f"https://t.me/{BOT_USERNAME}?start={token}"
    await m.reply(f"✅ Stored (24h)\n🔗 `{link}`")


@bot.on_message(filters.command("pay"))
async def pay(c, m):
    trx = m.text.split()[1]
    add_payment(m.from_user.id, trx)
    await m.reply("✅ Payment submitted. Await approval.")


@bot.on_message(filters.command("start") & filters.regex(r"start\s"))
async def getfile(c, m):
    token = m.text.split()[-1]
    f = get_file(token)
    if not f:
        return await m.reply("❌ Link expired or invalid")

    if is_premium(m.from_user.id):
        await c.forward_messages(m.chat.id, FORCE_SUB_CHANNEL, f["fid"])
    else:
        short = requests.get(
            SHORTENER_BASE_URL,
            params={"api": SHORTENER_API_KEY, "url": m.text}
        ).json().get("shortenedUrl")
        await m.reply(f"🔐 Watch Ad:\n{short}")


keep_alive()
bot.run()