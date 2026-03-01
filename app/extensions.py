import os
from collections import deque

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

_client = None
_events_collection = None
_fallback_events = deque(maxlen=200)


def _mongo_uri():
    uri = os.getenv("MONGO_URI") or "mongodb://localhost:27017"
    if not uri.strip() or uri.strip() == "your_mongodb_connection_string":
        return "mongodb://localhost:27017"
    return uri


def get_events_collection():
    global _client, _events_collection
    if _events_collection is not None:
        return _events_collection
    _client = MongoClient(_mongo_uri(), serverSelectionTimeoutMS=2000)
    _events_collection = _client["github_webhook_db"]["events"]
    return _events_collection


def fallback_insert_event(document):
    _fallback_events.appendleft(document)


def fallback_list_events(limit=20):
    return list(_fallback_events)[:limit]
