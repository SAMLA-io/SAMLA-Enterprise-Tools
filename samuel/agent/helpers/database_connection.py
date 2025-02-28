# Written by Juan Pablo Gutiérrez
# 27 01 2025
# This file is used to connect to the database and get the chat history

from datetime import datetime
from ..setup import MONGO_AWS_URL, MONGO_CHAT_HISTORY_COLLECTION, MONGO_AWS_TOKEN

import aiohttp
import requests
import json

def get_chat_history(company_id: str, user_id: str, include_response: bool = True):
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
        if not include_response:
            entry.pop("response")

    return full_database

async def insert_chat_history_async(company_id: str, session_id: str, user_id: str, user_message: str, agent_message: str):
    """
    Insert a message into the chat history asynchronously.
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{MONGO_AWS_URL}/insert_one", json={
            "database": company_id,
            "collection": MONGO_CHAT_HISTORY_COLLECTION,
            "data": {
                "session_id": session_id,
                "timestamp": str(datetime.now()),
                "user_id": user_id,
                "message": user_message,
                "response": agent_message
            }
        }, headers={"Authorization": f"Bearer {MONGO_AWS_TOKEN}", "Content-Type": "application/json"}) as response:
            return await response.text()
