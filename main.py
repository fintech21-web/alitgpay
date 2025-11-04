import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- Environment Variables ---
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # e.g., https://your-render-url.onrender.com

# --- Flask App ---
flask_app = Flask(__name__)

# --- Telegram Bot Setup ---
bot = Bot(TOKEN)
app = ApplicationBuilder().bot(bot).build()

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 እንኳን ደህና መጡ!\n\n"
        "የካናዳ ፕሮሰስ በስራ እና ክህሎት ሚንስቴር በኩል ለመጀመር "
        "የመመዝገቢያ ክፍያዎን ይክፈሉ።\n"
        "ለመክፈል ይህን ይጫኑ: /pay"
    )

# /pay command - professional formatted message
async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "💰 *የክፍያ መመሪያ* 💰\n\n"
        "እባክህ ክፍያዎን ከታች በተገለጸው መልኩ ይላኩ።\n\n"
        "------------------------------\n"
        "🏦 *የባንክ መረጃ* 🏦\n"
        "------------------------------\n"
        "• የአካውንት ስም : ዶ/ር አለምነህ ከፍያለው\n"
        "• የአካውንት ቁጥር : 1000489297275\n"
        "• የባንክ ስም : የኢትዮጵያ ንግድ ባንክ\n\n"
        "------------------------------\n"
        "📥 *ክፍያ ከተከፈለ* 📥\n"
        "ክፍያዎን ከከፈሉ በኋላ የክፍያ ደረሰኙን በዚህ የTelegram መንገድ @bkuelmis ይላኩ።\n\n"
        "------------------------------\n"
        "🙏 እናመሰግናለን ስለ ጥሩ ግንኙነትዎ!"
    )
    await update.message.reply_text(message, parse_mode="Markdown")

# Add handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("pay", pay))

# Webhook route
@flask_app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    app.update_queue.put(update)
    return "OK"

# Health check route
@flask_app.route("/", methods=["GET"])
def index():
    return "Bot is running!"

# Set webhook automatically
bot.set_webhook(WEBHOOK_URL + "/" + TOKEN)

# Run Flask server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)
