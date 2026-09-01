import os

_client = None
_collection = None

try:
    from pymongo import MongoClient

    mongo_url = os.getenv("MONGODB_URI")
    if mongo_url:
        _client = MongoClient(mongo_url, serverSelectionTimeoutMS=1500)
        _client.admin.command("ping")
        _collection = _client[os.getenv("MONGODB_DB", "docvoice")]["documents"]
except Exception:
    _client = None
    _collection = None


def save_document(document: dict):
    if _collection is not None:
        _collection.insert_one(document)
