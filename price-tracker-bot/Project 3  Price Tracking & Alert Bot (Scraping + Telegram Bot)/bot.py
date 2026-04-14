from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from scraper import scrape_product
from db import save_product

TOKEN = "8737056098:AAH7SAPRF_99j1NRJiHZpZKk6WuRGkneUaw"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Use /track <url> <target_price>")

async def track(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) < 2:
            await update.message.reply_text("Usage: /track <url> <target_price>")
            return

        url = context.args[0]
        target_price = context.args[1]

        data = await scrape_product(url)
        print("Scraped data:", data)  # Debug log

        save_product(update.message.chat_id, url, data["title"], data["price"], target_price)
        await update.message.reply_text(f"Tracking {data['title']} at {data['price']}")
    except Exception as e:
        print("Bot error:", e)
        await update.message.reply_text(f"Error: {e}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("track", track))
    app.run_polling()

if __name__ == "__main__":
    main()

