import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# =========================
# CONFIG
# =========================
BOT_TOKEN = "7791954489:AAFa3EZrEsTFCGiqL4bS0cCYDMCRQTm2KG0"  
API_URL = "http://127.0.0.1:8000/api/crews"  

# /kru command
async def kru_index(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        page = 1
        per_page = 20
        sort_by = "atk"
        order = "desc"
        filters = {}  # awalnya kosong

        # Ambil data dari backend
        params = {
            "page": page,
            "per_page": per_page,
            "sort_by": sort_by,
            "order": order,
            **filters
        }
        res = requests.get(API_URL, params=params)
        if res.status_code == 200:
            data = res.json()
            crews = data.get('data', [])

            if not crews:
                await update.message.reply_text("Belum ada kru.")
                return

            # Buat teks daftar kru dengan info sorting
            text = "---Daftar Kru---\n\n"
            text += "\n".join(crews)

            # Inline keyboard hanya untuk class
            keyboard = [
                [
                    InlineKeyboardButton("SSS", callback_data="filter_class_SSS"),
                    InlineKeyboardButton("SS", callback_data="filter_class_SS"),
                    InlineKeyboardButton("S", callback_data="filter_class_S"),
                ],
                [
                    InlineKeyboardButton("A", callback_data="filter_class_A"),
                    InlineKeyboardButton("B", callback_data="filter_class_B"),
                    InlineKeyboardButton("C", callback_data="filter_class_C"),
                ],
                [
                    InlineKeyboardButton("D", callback_data="filter_class_D"),
                    InlineKeyboardButton("E", callback_data="filter_class_E"),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(text, reply_markup=reply_markup)
        else:
            await update.message.reply_text("Gagal ambil data kru.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def kru_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # wajib, agar loading stop di Telegram

    data = query.data  # misal: "filter_class_SS"
    if data.startswith("filter_class_"):
        class_value = data.split("_")[-1]  # ambil SS/SSS/S...
        params = {
            "page": 1,
            "per_page": 20,
            "sort_by": "atk",
            "order": "desc",
            "class": class_value
        }

        res = requests.get(API_URL, params=params)
        if res.status_code == 200:
            crews = res.json().get("data", [])
            text = "---Daftar Kru---\n\n"
            text += "\n".join(crews) if crews else "Belum ada kru."

            # edit message lama
            await query.edit_message_text(text, reply_markup=query.message.reply_markup)

async def show_kru(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text.startswith('/'):
        return

    data = text.lstrip('/')  # ambil command tanpa "/"
    print(f"Command diterima: {data}")
    try:
        res = requests.get(f"{API_URL}/{data}")
        print(res)
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
async def store_kru(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    app.add_handler(CommandHandler("kru", kru_index))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^/kru_\S+'), show_kru))
    app.add_handler(MessageHandler(filters.ALL, store_kru))
    app.add_handler(CallbackQueryHandler(kru_callback))
    
    print("Bot jalan...")
    app.run_polling()

if __name__ == "__main__":
    main()