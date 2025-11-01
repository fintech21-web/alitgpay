import os
import threading
import time
import requests
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Initialize Flask
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "✅ Bot is running!"

# Telegram bot setup
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

telegram_app = ApplicationBuilder().token(TOKEN).build()
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("pay", pay))

# Keep-alive function
def keep_alive():
    url = os.getenv("RENDER_URL")
    if not url:
        print("⚠️ No RENDER_URL set; skipping keep-alive pings.")
        return
    while True:
        try:
            requests.get(url)
            print(f"🔁 Pinged {url} to stay awake.")
        except Exception as e:
            print("Ping failed:", e)
        time.sleep(300)  # Ping every 5 minutes

# Run both Flask and Telegram bot together
def run_bot():
    print("Starting Telegram bot...")
    telegram_app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    threading.Thread(target=keep_alive).start()
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)
