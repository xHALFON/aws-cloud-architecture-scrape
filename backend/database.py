from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def connect_to_mongo():
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("DB_NAME")

    if not mongo_uri or not db_name:
        raise ValueError("Missing MONGO_URI or DB_NAME in .env")

    client = MongoClient(mongo_uri)
    db = client[db_name]
    print("✅ Connected to MongoDB")
    return db