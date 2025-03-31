# Written by Juan Pablo Gutiérrez
# 23 01 2025

import requests
from ..setup import RAG_URL

def get_rag_context(organization_id: str, prompt: str):
    url = f"{RAG_URL}/search?organization_id={organization_id}&prompt={prompt}"
    context = requests.post(url)
    
    context_list = []
    for chunk in context.json():
        context_list.append(chunk["fields"]["content"])
    
    return "\n".join(context_list)
