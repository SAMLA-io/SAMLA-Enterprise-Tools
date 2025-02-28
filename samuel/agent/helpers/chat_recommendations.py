# Written by Juan Pablo Gutiérrez
# 27 01 2025

from ..helpers.prompting import ask
from ..helpers.database_connection import get_chat_history
import json

async def get_chat_recommendations(company_id: str, user_id: str, session_id: str):
    chat_history = get_chat_history(company_id, user_id, include_response=False)

    prompt = f"""
        Based on this chat history, generate 5 chat questions recommendations that will suit the user's needs. Write it in a json list format, not markdown.
        Chat history: {chat_history}
    """
    
    response = await ask(company_id=company_id, user_id=user_id, session_id=session_id, prompt=prompt, rag=False, insert_history=False)

    return response