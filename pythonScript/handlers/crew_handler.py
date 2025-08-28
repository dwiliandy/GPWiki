import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.crew_service import get_crews, get_crew_detail

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
            "============================\n"
            "🏴‍☠️ Data Kru 🏴‍☠️\n"
            "============================\n\n"
            f"{crew.get('type_emoji')} {crew.get('name')}\n\n"
            "ℹ️ Informasi:\n"
            f" Type : {crew.get('type')}\n"
            f" Class: {crew.get('class')}\n\n"
            "📊 Statistik:\n"
            f" ➕ ATK   : {crew.get('atk')}\n"
            f" ➕ DEF   : {crew.get('def')}\n"
            f" ➕ HP    : {crew.get('hp')}\n"
            f" ➕ SPEED : {crew.get('speed')}"
        )
        await update.message.reply_text(msg)
    else:
        await update.message.reply_text("⚠️ Kru tidak ditemukan")

