from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from scraper import scrape_startech

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a search query. Usage: /search Mac Mini m4")
        return
    query = ' '.join(context.args)
    await update.message.reply_text(f"🔍 Searching for {query} on Startech...")
    products = scrape_startech(query)
    if not products:
        await update.message.reply_text("No products found.")
        return
    for product in products:
        caption = f"{product['name']}\nLink: {product['link']}\nPrice: {product['price']}"
        if product['img']:
            await update.message.reply_photo(photo=product['img'], caption=caption)
        else:
            await update.message.reply_text(caption)

if __name__ == '__main__':
    app = ApplicationBuilder().token('8755115761:AAHQ_rpauieTwXtjKushG6IDKB3B8zO4ifU').build()
    app.add_handler(CommandHandler("search", search_command))
    print("Bot is running...")
    app.run_polling()