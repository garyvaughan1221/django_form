"""
Test script to verify MongoDB connection using the helper in mongo_conn.py.
This will print database names available to the configured user.

Usage (PowerShell):
python .\test_mongo_connect.py
"""
from mongo_conn import get_client, get_db, close_client
import sys


def main():
    try:
        client = get_client()
        print("Connected to MongoDB server:", client.address)

        # If MONGODB_DB is set, show collections in that DB. Else list DB names.
        import os
        db_name = "2020USRC"
        if db_name:
            db = get_db()
            print(f"Using DB: {db_name}")
            print("Collections:", db.list_collection_names())
        else:
            print(f"Using DB: {db_name}")
            print("No MONGODB_DB set — listing database names visible to this user:")
            print(client.list_database_names())

    except Exception as e:
        print("Error connecting to MongoDB:", e, file=sys.stderr)
        sys.exit(2)
    finally:
        close_client()


if __name__ == '__main__':
    main()