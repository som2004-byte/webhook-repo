from __future__ import annotations

import os
from collections import deque
from typing import Any, Deque, Dict, List, Optional

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection

# Load .env from project root (parent of app/), regardless of CWD.
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

_client: Optional[MongoClient] = None
_events_collection: Optional[Collection] = None

# In-memory fallback so the app still works without MongoDB running.
_fallback_events: Deque[Dict[str, Any]] = deque(maxlen=200)


def _mongo_uri() -> str:
    uri = os.getenv("MONGO_URI") or "mongodb://localhost:27017"
    if uri.strip() == "your_mongodb_connection_string":
        return "mongodb://localhost:27017"
    return uri


def get_events_collection() -> Collection:
    """
    Lazily creates and returns the MongoDB collection.

    Note: This does not force a connection on creation; operations may still fail
    if MongoDB is not running. Routes should handle those errors gracefully.
    """
    global _client, _events_collection

    if _events_collection is not None:
        return _events_collection

    _client = MongoClient(
        _mongo_uri(),
        # Fail fast when MongoDB isn't reachable, instead of hanging.
        serverSelectionTimeoutMS=2000,
        connectTimeoutMS=2000,
        socketTimeoutMS=2000,
    )
    db = _client["github_webhook_db"]
    _events_collection = db["events"]
    return _events_collection


def fallback_insert_event(document: Dict[str, Any]) -> None:
    _fallback_events.appendleft(document)


def fallback_list_events(limit: int = 20) -> List[Dict[str, Any]]:
    return list(_fallback_events)[:limit]