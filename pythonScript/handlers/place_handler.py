from telegram import Update
from telegram.ext import ContextTypes
from services.place_service import get_places

async def place_index(update: Update, context: ContextTypes.DEFAULT_TYPE):
    places = get_places()
    if not places:
        await update.message.reply_text("Belum ada tempat.")
        return

    text = "---Daftar Tempat---\n\n" + "\n".join([p["name"] for p in places])
    await update.message.reply_text(text)
