import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

# Bot token from environment variable
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID", None)  # Admin Chat ID (optional)

# Dummy HTTP server to satisfy Render's port binding requirement
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))  # Default port is 8080
    server = HTTPServer(("0.0.0.0", port), DummyHandler)
    print(f"Dummy server running on port {port}")
    server.serve_forever()

# Bot Handlers
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "🤖 Welcome to Codesaif Store Bot!\n"
        "Use the buttons or commands to navigate."
    )

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Here's what I can do:\n"
        "/start - Start the bot\n"
        "/help - Get help\n"
        "/store - View products\n"
        "/contact - Contact admin"
    )

def store(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "🛒 Welcome to our store!\n\n"
        "1. Product A - $50 [Buy](https://store.codesaif.in/product-a)\n"
        "2. Product B - $100 [Buy](https://store.codesaif.in/product-b)\n"
        "3. Product C - $200 [Buy](https://store.codesaif.in/product-c)\n\n"
        "More at: [Store](https://store.codesaif.in)"
    )

def handle_text(update: Update, context: CallbackContext) -> None:
    message = update.message.text.lower()
    if message in ["hi", "hello"]:
        update.message.reply_text("Hello! How can I help you today?")
    elif message in ["thanks", "thank you"]:
        update.message.reply_text("You're welcome! 😊")
    elif message in ["buy", "purchase"]:
        update.message.reply_text("Check out our store here: [Store](https://store.codesaif.in)")
    else:
        # Forward other messages to the admin
        if ADMIN_CHAT_ID:
            context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Message from {update.message.chat.id}: {update.message.text}")
            update.message.reply_text("Your message has been forwarded to the admin.")
        else:
            update.message.reply_text("I didn't understand that. Use /help to see available commands.")

# Main Function
def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('store', store))

    # Add message handler for text
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    # Start the bot in a separate thread
    Thread(target=updater.start_polling).start()

    # Start dummy HTTP server
    run_dummy_server()

if __name__ == '__main__':
    main()
