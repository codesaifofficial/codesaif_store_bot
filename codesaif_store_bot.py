import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

# Bot token environment variable se fetch karein
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = '6481511626'  # Replace with your actual Admin Chat ID

# /start Command ka function
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Welcome to Codesaif Store Bot!\n\n"
        "Use /help to get a list of available commands.\n"
        "Use /store to view our products."
    )

# /help Command ka function
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Here are some commands you can use:\n"
        "/start - Start the bot\n"
        "/help - Get help\n"
        "/store - View store products\n"
        "/contact - Get contact info"
    )

# /store Command ka function
def store(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Welcome to our store! Here are our top products:\n\n"
        "1. 1000+ course bundle - $10\n"
        "2. premuim tools - $0\n"
        "3. digital product store - view-store\n\n"
        "For more details, visit our website: codesaif.in"
    )

# /contact Command ka function
def contact(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "You can reach us at:\n"
        "Email: support@codesaif.in\n"
        "Phone: +918750577291\n"
        "Website: www.codesaif.in"
    )

# Custom message handler for specific keywords
def custom_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text.lower()  # User's message in lowercase
    if 'hello' in user_message:
        update.message.reply_text("Hello! How can I assist you today?")
    elif 'help' in user_message:
        update.message.reply_text("I can help you with:\n/start - Start the bot\n/store - View our products\n/contact - Get contact info")
    else:
        update.message.reply_text("Sorry, I didn't understand that. Type 'help' for a list of commands.")

# Forward user messages to admin
def forward_to_admin(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    user_name = update.message.from_user.name
    # Forward message to admin
    context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Message from {user_name}: {user_message}")
    # Reply to user
    update.message.reply_text("Your message has been forwarded to the admin.")

# Main function jo bot ko run karega
def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Commands ke liye handlers add karein
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('store', store))
    dispatcher.add_handler(CommandHandler('contact', contact))

    # Custom message handling and forwarding to admin
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, custom_message))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, forward_to_admin))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
