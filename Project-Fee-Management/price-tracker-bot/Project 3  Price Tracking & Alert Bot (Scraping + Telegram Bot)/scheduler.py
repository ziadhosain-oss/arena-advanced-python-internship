import asyncio
import time
from scraper import scrape_product
from db import get_all_products, save_product
from telegram import Bot

TOKEN = "8737056098:AAH7SAPRF_99j1NRJiHZpZKk6WuRGkneUaw"
bot = Bot(token=TOKEN)

async def check_prices():
    products = get_all_products()
    for p in products:
        data = await scrape_product(p["url"])
        new_price = data["price"]
        save_product(p["user_id"], p["url"], data["title"], new_price, p["target_price"])

        try:
            new_price_num = float(new_price.replace(",", "").replace("৳", "").strip())
            target_price_num = float(p["target_price"])
            if new_price_num < target_price_num:
                await bot.send_message(chat_id=p["user_id"], text=f"Price drop! {data['title']} is now {new_price}")
        except:
            pass

if __name__ == "__main__":
    while True:
        asyncio.run(check_prices())
        time.sleep(6 * 60 * 60)  # every 6 hours
