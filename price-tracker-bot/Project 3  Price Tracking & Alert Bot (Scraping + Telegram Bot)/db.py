from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["price_tracker"]
products = db["products"]

def save_product(user_id, url, title, price, target_price):
    products.update_one(
        {"url": url, "user_id": user_id},
        {"$set": {"title": title, "current_price": price, "target_price": target_price},
         "$push": {"history": {"price": price}}},
        upsert=True
    )

def get_all_products():
    return list(products.find())



