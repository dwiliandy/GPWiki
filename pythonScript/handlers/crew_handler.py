import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.crew_service import get_crews, get_crew_detail, store_crews

async def kru_index(update: Update, context: ContextTypes.DEFAULT_TYPE):
    crews = get_crews({"page": 1, "per_page": 20, "sort_by": "atk", "order": "desc"})
    if not crews:
        await update.message.reply_text("Belum ada kru.")
        return

    text = "---Daftar Kru---\n\n"
    text += "\n".join(crews)

    keyboard = [
        [InlineKeyboardButton("SSS", callback_data="filter_class_SSS"),
         InlineKeyboardButton("SS", callback_data="filter_class_SS")],
        [InlineKeyboardButton("S", callback_data="filter_class_S"),
         InlineKeyboardButton("A", callback_data="filter_class_A")]
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def show_kru(update: Update, context: ContextTypes.DEFAULT_TYPE):
    crew_id = update.message.text.lstrip("/")
    crew = get_crew_detail(crew_id)
    if crew:
        msg = (
            f"{crew.get('type_emoji')} Kru: {crew.get('name')} ({crew.get('class')})\n"
            f"Type: {crew.get('type')}\n"
            f"ATK: {crew.get('atk')}, DEF: {crew.get('def')}, "
            f"HP: {crew.get('hp')}, SPEED: {crew.get('speed')}"
        )
        await update.message.reply_text(msg)
    else:
        await update.message.reply_text("⚠️ Kru tidak ditemukan")

async def store_kru(update: Update, context: ContextTypes.DEFAULT_TYPE):
    content = update.message.text or update.message.caption or ""
    if "Daftar Kru Dimiliki" in content:
        res = store_crews(content)
        if res.status_code in [200, 201]:
            await update.message.reply_text("✅ Kru berhasil disimpan")
        else:
            await update.message.reply_text("⚠️ Gagal simpan kru")
