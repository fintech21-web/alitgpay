import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- Telegram Bot Setup ---
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Type /pay to get payment details.")

async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "💰 *Payment Details:*\n\n"
        "Please send your payment to this account:\n\n"
        "🏦 Account Name: Fintech Invest\n"
        "💳 Account Number: 1234567890\n"
        "🏦 Bank: CBE\n\n"
        "After payment, send your receipt here."
    )
    await update.message.reply_text(message, parse_mode="Markdown")

# --- Flask App Setup (to keep Render service alive) ---
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)

# Start Flask in a background thread
threading.Thread(target=run_flask, daemon=True).start()

# --- Start the Telegram Bot ---
print("Starting Telegram bot...")
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("pay", pay))
app.run_polling()
