# Written by Juan Pablo Gutiérrez
# 27 01 2025
# This file is used to connect to the database and get the chat history

import requests
from ..setup import MONGO_AWS_URL, MONGO_CHAT_HISTORY_COLLECTION, MONGO_AWS_TOKEN

def get_chat_history(company_id: str):
    """
    Get the chat history from the database. 
    
    This is the only function that directly calls the database. 
    """
    full_database = requests.get(f"{MONGO_AWS_URL}/get_all", params={
        "database": company_id,
        "collection": MONGO_CHAT_HISTORY_COLLECTION
    },
    headers={"Authorization": f"Bearer {MONGO_AWS_TOKEN}", "Content-Type": "application/json"}
    )

    # Reduce the size of the entries to only 10 entries
    full_database = full_database.json()[:10]

    return full_database