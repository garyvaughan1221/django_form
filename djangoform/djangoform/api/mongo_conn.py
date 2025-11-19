"""
Simple MongoDB connection helper using pymongo.
Reads connection settings from environment variables:
- MONGODB_URI (default: mongodb://localhost:27017)
- MONGODB_DB (optional default DB name)

Usage:
from mongo_conn import get_db
db = get_db()  # returns a Database instance
"""
from typing import Optional
import os
from pymongo import MongoClient

_client: Optional[MongoClient] = None
_default_db_name: Optional[str] = "2020USRC"


## this is a readOnly account caged to the 2020USRC database
def _get_uri() -> str:
    return os.environ.get("MONGODB_URI", "mongodb+srv://mongodb_readOnly:dwg4TZoXgjCY30N6@pythonprojects.i22ru0h.mongodb.net/")


def _get_db_name() -> Optional[str]:
    return os.environ.get("MONGODB_DB")


def get_client() -> MongoClient:
    """Return a (cached) MongoClient instance.

    The client is cached for the process lifetime. Call close_client() to close.
    """
    global _client, _default_db_name
    if _client is None:
        uri = _get_uri()
        _client = MongoClient(uri)
        _default_db_name = "2020USRC"
    return _client


def get_db(db_name: Optional[str] = None):
    """Return a pymongo.database.Database object.

    If db_name is not provided, uses MONGODB_DB env var. If that's not set,
    raises ValueError so callers are explicit about which DB to use.
    """
    client = get_client()
    name = db_name or _default_db_name
    if not name:
        raise ValueError(
            "No database name provided. Set MONGODB_DB environment variable or pass db_name."
        )
    return client[name]


def close_client() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None
