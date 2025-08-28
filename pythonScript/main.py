import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from config import BOT_TOKEN
from handlers.crew_handler import kru_index, show_kru
from handlers.place_handler import place_index
from handlers.store_handler import storeData

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Main handlers
    app.add_handler(CommandHandler("kru", kru_index))
    app.add_handler(CommandHandler("place", place_index))

    #kru
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^/kru_\S+'), show_kru))
    
    # Store
    app.add_handler(MessageHandler(filters.ALL, storeData))
    print("Bot jalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
