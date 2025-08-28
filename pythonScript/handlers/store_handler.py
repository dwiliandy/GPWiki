
from telegram import Update
from telegram.ext import ContextTypes
from services.crew_service import store_crews
from services.place_service import store_places

async def storeData(update: Update, context: ContextTypes.DEFAULT_TYPE):
    content = update.message.text or update.message.caption or ""
    print("Daftar Kru Dimiliki" in content)
    if "Daftar Kru Dimiliki" in content:
        res = store_crews(content)
        try:
            data = res.json()
            message = data.get("message", "✅ Berhasil diproses")
        except Exception:
            message = "❌ Terjadi kesalahan, tidak ada response JSON."       # isi raw error dari server
        await update.message.reply_text(message)
    
    if "Travel - GrandPirates" in content:
        res = store_places(content)
        try:
            data = res.json()
            message = data.get("message", "✅ Berhasil diproses")
        except Exception:
            message = "❌ Terjadi kesalahan, tidak ada response JSON."       # isi raw error dari server
        await update.message.reply_text(message)