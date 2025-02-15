# Written by Juan Pablo Gutiérrez
# 27 01 2025
# This file is used to connect to the database and get the chat history

from datetime import datetime
import requests
import json
from ..setup import MONGO_AWS_URL, MONGO_CHAT_HISTORY_COLLECTION, MONGO_AWS_TOKEN

def get_chat_history(company_id: str, user_id: str):
    """
    Get the chat history from the database. 
    
    This is the only function that directly calls the database. 
    """
    full_database = requests.get(f"{MONGO_AWS_URL}/get_many", params={
        "database": company_id,
        "collection": MONGO_CHAT_HISTORY_COLLECTION,
        "query": json.dumps({"user_id": user_id})
    },
    headers={"Authorization": f"Bearer {MONGO_AWS_TOKEN}", "Content-Type": "application/json"}
    )

    full_database = full_database.json()

    full_database = sorted(full_database, key=lambda x: x["timestamp"])
    full_database = full_database[:10]

    # Removes unnecessary fields
    for entry in full_database:
        entry.pop("user_id")
        entry.pop("session_id")
        entry.pop("timestamp")
        entry.pop("_id")

    return full_database

def insert_chat_history(company_id: str, session_id: str, user_id: str, message: str):
    """
    Insert a message into the chat history.
    """
    requests.post(f"{MONGO_AWS_URL}/insert_one", json={
        "database": company_id,
        "collection": MONGO_CHAT_HISTORY_COLLECTION,
        "data": {
            "session_id": session_id,
            "timestamp": str(datetime.now()),
            "user_id": user_id,
            "message": message,
        }
    },
    headers={"Authorization": f"Bearer {MONGO_AWS_TOKEN}", "Content-Type": "application/json"}
    ) 
    