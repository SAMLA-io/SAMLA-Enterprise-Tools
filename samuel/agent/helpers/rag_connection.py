# Written by Juan Pablo Gutiérrez
# 23 01 2025

import requests
from ..setup import RAG_URL, RAG_COLLECTION

def get_rag_context(company_id: str, prompt: str):
    context = requests.get(f"{RAG_URL}/get_context", params={
            "database": company_id,
            "collection": RAG_COLLECTION,
            "query": prompt
        })

    return context.json()["body"]
