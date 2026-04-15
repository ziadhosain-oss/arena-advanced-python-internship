from pymongo import MongoClient
try:
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print('MongoDB connection successful')
except Exception as e:
    print(f'MongoDB connection failed: {e}')