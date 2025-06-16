from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_USERNAME = os.environ.get("MONGODB_USERNAME")
MONGODB_PASSWORD = os.environ.get("MONGODB_PASSWORD")
MONGODB_DB = os.environ.get("MONGODB_DB")
MONGODB_HOST = os.environ.get("MONGODB_HOST")

mongo_uri = f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}:27017/{MONGODB_DB}?authSource=admin"
client = MongoClient(mongo_uri)

def check_connection():
    try:
        client.admin.command('ping')
        print("✅ Connected to MongoDB successfully.")
    except ConnectionFailure as e:
        print("❌ Failed to connect to MongoDB:", e)
        import sys
        sys.exit(1)

db = client[MONGODB_DB]
users_collection = db.users