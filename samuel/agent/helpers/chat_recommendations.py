# Written by Juan Pablo Gutiérrez
# 27 01 2025

from ..helpers.prompting import ask
from ..helpers.database_connection import get_chat_history

async def get_chat_recommendations(organization_id: str, user_id: str, session_id: str):
    chat_history = get_chat_history(organization_id, user_id, include_response=False)

    prompt = f"""
        Based on this chat history, generate 5 chat questions recommendations that will suit the user's needs. Write it in a json list format, not markdown.
        Chat history: {chat_history}
    """
    
    response, response_time, context_time, chat_history_time, insert_history_time = await ask(organization_id=organization_id, user_id=user_id, session_id=session_id, prompt=prompt, rag=False, insert_history=False)

    return response, response_time, context_time, chat_history_time, insert_history_time