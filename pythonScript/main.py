import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# =========================
# CONFIG
# =========================
BOT_TOKEN = "7791954489:AAFa3EZrEsTFCGiqL4bS0cCYDMCRQTm2KG0"  
API_URL = "http://127.0.0.1:8000/api/crews"  

# /kru command
async def kru_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        res = requests.get(f"{API_URL}/{crew_id}")  # GET /api/crews/{id}
        if res.status_code == 200:
            data = res.json()

            # Ambil array dari key 'data' (sesuai controller Laravel sebelumnya)
            crews = data.get('data', [])

            if not crews:
                await update.message.reply_text("Belum ada kru.")
            else:
                # Tampilkan langsung tiap item dalam list
                text = "\n".join(crews)
                await update.message.reply_text(text)

        else:
            await update.message.reply_text("Gagal ambil data kru.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")


async def crew_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text.startswith('/'):
        return

    data = text.lstrip('/')  # ambil command tanpa "/"
    try:
        res = requests.get(f"{API_URL}{data}")
        if res.status_code == 200:
            crew = res.json().get('data')
            msg = (
                f"{crew.get('type_emoji')} Kru: {crew.get('name')} ({crew.get('class')})\n"
                f"Type: {crew.get('type')}\n"
                f"ATK: {crew.get('atk')}, DEF: {crew.get('def')}, HP: {crew.get('hp')}, SPEED: {crew.get('speed')}"
            )

            await update.message.reply_text(msg)
        else:
            msg = res.json().get('message', 'Crew tidak ditemukan')
            await update.message.reply_text(f"⚠️ {msg}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# Handler untuk pesan forward
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    # Ambil text atau caption
    content = update.message.text or update.message.caption or ""
    logging.info(f"Terima pesan: {content}")

    if "Daftar Kru Dimiliki" in content:
        try:
            res = requests.post(API_URL, data={"raw_text": content})
            if res.status_code in [200, 201]:
                await update.message.reply_text("✅ Kru berhasil disimpan")
            else:
                # Ambil pesan dari backend
                data = res.json()
                await update.message.reply_text(f"⚠️ {data.get('message', 'Gagal simpan kru')}")
        except Exception as e:
            await update.message.reply_text(f"Error: {e}")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("kru", kru_handler))
    app.add_handler(MessageHandler(filters.ALL, message_handler))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^/'), crew_command))
    
    print("Bot jalan...")
    app.run_polling()

if __name__ == "__main__":
    main()