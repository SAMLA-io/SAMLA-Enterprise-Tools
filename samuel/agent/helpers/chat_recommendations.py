# Written by Juan Pablo Gutiérrez
# 27 01 2025

from ..helpers.prompting import ask
from ..helpers.database_connection import get_chat_history

def get_chat_recommendations(company_id: str):
    chat_history = get_chat_history(company_id)

    prompt = f"""
        Based on this chat history, generate 5 chat recommendations that will suit the user's needs
        Chat history: {chat_history}
    """

    response = ask(company_id, prompt, rag=False)

    return response