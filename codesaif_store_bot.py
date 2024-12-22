import os
import random
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters

# Bot token and admin chat ID
TOKEN = os.getenv("BOT_TOKEN")  # Ensure BOT_TOKEN is set in Render environment variables
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")  # Set your admin chat ID in Render environment variables

# Flask app for dummy server
app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is running!"

# Welcome Menu
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("🛒 View Store", callback_data='view_store')],
        [InlineKeyboardButton("👤 Contact Admin", callback_data='contact_admin')],
        [InlineKeyboardButton("❓ FAQ", callback_data='faq')],
        [InlineKeyboardButton("💬 Support", callback_data='support')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "🤖 *Welcome to Codesaif Store Bot!*\n\nChoose an option below:",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )

# View Store
def view_store(update: Update, context: CallbackContext) -> None:
    categories = ["E-books", "Courses", "Tools"]
    keyboard = [[InlineKeyboardButton(cat, callback_data=f'category_{cat.lower()}')] for cat in categories]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text(
        "🛒 *Choose a category:*",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )

# Handle Product Categories
def handle_categories(update: Update, context: CallbackContext) -> None:
    category = update.callback_query.data.split("_")[1].capitalize()
    products = [
        {"name": f"{category} Product 1", "price": "$50", "link": "https://store.codesaif.in/product1"},
        {"name": f"{category} Product 2", "price": "$100", "link": "https://store.codesaif.in/product2"},
        {"name": f"{category} Product 3", "price": "$200", "link": "https://store.codesaif.in/product3"}
    ]

    for product in products:
        keyboard = [[InlineKeyboardButton("Buy Now", url=product['link'])]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text(
            f"💼 *{product['name']}*\n💰 Price: {product['price']}",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

# FAQ Section
def faq(update: Update, context: CallbackContext) -> None:
    faq_text = (
        "❓ *FAQs*\n\n"
        "1. *How to Buy?*\nVisit the store and click 'Buy Now'.\n\n"
        "2. *Refund Policy?*\nRefunds are available within 7 days.\n\n"
        "3. *Contact Support?*\nUse /support to report an issue."
    )
    update.callback_query.message.reply_text(faq_text, parse_mode=ParseMode.MARKDOWN)

# Support Ticket System
def support(update: Update, context: CallbackContext) -> None:
    ticket_id = f"SUP{random.randint(1000, 9999)}"
    update.message.reply_text(
        f"🎟️ *Support Ticket Created!*\n\nYour ticket ID is: `{ticket_id}`.\nOur team will contact you soon.",
        parse_mode=ParseMode.MARKDOWN
    )

# Handle User Messages
def handle_user_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text.lower()
    pre_defined_responses = {
        "hi": "Hello! How can I assist you today?",
        "hello": "Hi there! Need any help?",
        "thanks": "You're welcome!",
        "buy": "Check out our store here: https://store.codesaif.in"
    }

    if user_message in pre_defined_responses:
        update.message.reply_text(pre_defined_responses[user_message])
    else:
        # Forward non-predefined messages to Admin
        if ADMIN_CHAT_ID:
            context.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=f"📩 New Message from @{update.message.chat.username}:\n\n{user_message}"
            )
        update.message.reply_text(
            "Your message has been forwarded to the admin. Please wait for a reply!"
        )

# Callback Handlers
def handle_callbacks(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    if query.data == "view_store":
        view_store(update, context)
    elif query.data.startswith("category_"):
        handle_categories(update, context)
    elif query.data == "faq":
        faq(update, context)
    elif query.data == "contact_admin":
        query.message.reply_text(
            "👤 *Contact Admin*\n\nSend your message directly, and we'll get back to you!"
        )

# Main Function
def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Command Handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('support', support))

    # Callback Handlers
    dispatcher.add_handler(CallbackQueryHandler(handle_callbacks))

    # Message Handlers
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_user_message))

    # Start Polling in a separate thread
    updater.start_polling()

    # Start the Flask server to keep the service alive
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

if __name__ == '__main__':
    main()
