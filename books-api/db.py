from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
# from dotenv import load_dotenv
import os

# load_dotenv()

MONGODB_USERNAME = os.environ.get("MONGODB_USERNAME")
MONGODB_PASSWORD = os.environ.get("MONGODB_PASSWORD")
MONGODB_DB = os.environ.get("MONGODB_DB")
MONGODB_HOST = os.environ.get("MONGODB_HOST")
APP_ENV = os.environ.get("APP_ENV", "production")

mongo_uri_dev = f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}:27017/{MONGODB_DB}?authSource=admin"
mongo_uri_prod = f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}/{MONGODB_DB}?retryWrites=true&w=majority"

if APP_ENV == "development":
    print("⚙️ Running in dev mode")
    client = MongoClient(mongo_uri_dev)
else:
    print("🚀 Running in production mode")
    client = MongoClient(mongo_uri_prod)

def check_connection():
    try:
        client.admin.command('ping')
        print("✅ Connected to MongoDB successfully.")
    except ConnectionFailure as e:
        print("❌ Failed to connect to MongoDB:", e)
        import sys
        sys.exit(1)

def get_db():
    db = client[MONGODB_DB]
    return db

def get_books_collection():
    return get_db().books