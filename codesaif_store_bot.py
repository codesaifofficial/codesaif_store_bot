import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

# Bot token environment variable se fetch karein
TOKEN = os.getenv("BOT_TOKEN")

# /start Command ka function
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Welcome to Codesaif Store Bot!\n\n"
        "Use /help to get a list of available commands.\n"
        "Use /store to view our products."
    )

# Baaki ka code as-is
# /help Command ka function
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Here are some commands you can use:\n"
        "/start - Start the bot\n"
        "/help - Get help\n"
        "/store - View store products\n"
        "/contact - Get contact info"
    )

# /store Command ka function (aapke store ke products dikhaane ke liye)
def store(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Welcome to our store! Here are our top products:\n\n"
        "1. Product 1 - $50\n"
        "2. Product 2 - $100\n"
        "3. Product 3 - $200\n\n"
        "For more details, visit our website."
    )

# /contact Command ka function (Contact information ke liye)
def contact(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "You can reach us at:\n"
        "Email: support@codesaif.com\n"
        "Phone: +1234567890\n"
        "Website: www.codesaif.com"
    )

# Default message handler (jab user koi bhi aur message bheje)
def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f"You said: {update.message.text}")

# Main function jo bot ko run karega
def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('store', store))
    dispatcher.add_handler(CommandHandler('contact', contact))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
