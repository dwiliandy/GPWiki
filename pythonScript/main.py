import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from config import BOT_TOKEN
from handlers.crew_handler import kru_index, show_kru, store_kru
from handlers.place_handler import place_index

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Crew handlers
    app.add_handler(CommandHandler("kru", kru_index))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^/kru_\S+'), show_kru))
    app.add_handler(MessageHandler(filters.ALL, store_kru))

    # Place handlers
    app.add_handler(CommandHandler("place", place_index))

    print("Bot jalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
