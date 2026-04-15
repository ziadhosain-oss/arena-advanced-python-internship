from pymongo import MongoClient
from flask_login import UserMixin

client = MongoClient('mongodb://localhost:27017/')
db = client['flask_scraper']

# products (scraped)
# users (authentication/login)

products_collection = db['products']
users_collection = db['users']

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.username = user_data['username']

def init_db():

    if not users_collection.find_one({'username': 'admin'}):
        users_collection.insert_one({
            'username': 'admin',
            'password': 'admin',
        })
    print("Database initialized with default admin user.")