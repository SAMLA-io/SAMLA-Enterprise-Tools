# Written by Juan Pablo Gutiérrez
# 23 01 2025

from agent.helpers.database_connection import get_chat_history, insert_chat_history_async
from ..setup import agent, execute_orchestrator
from fastapi import  UploadFile
from pypdf import PdfReader
from docx import Document
from ..helpers.rag_connection import get_rag_context

import pandas as pd
import asyncio
import time

async def ask(organization_id: str, user_id: str, session_id: str, prompt: str, rag: bool = True, insert_history: bool = True) -> str:
    start_time = time.time()
    context = ""
    if rag:
        context = get_rag_context(organization_id, prompt)
    context_time = time.time() - start_time

    start_time = time.time()
   
    chat_history = ""
    if session_id:
        chat_history = get_chat_history(organization_id, user_id, session_id)
    chat_history_time = time.time() - start_time

    start_time = time.time()
    new_prompt = f"Prompt: {prompt}\n"
    if context:
        new_prompt = f"Context: {context}\n" + new_prompt
    if chat_history:
        new_prompt = f"Chat history: {chat_history}\n" + new_prompt

    response = execute_orchestrator(new_prompt)
    response_time = time.time() - start_time

    start_time = time.time()    
    if insert_history:
        await insert_chat_history_async(organization_id, session_id, user_id, prompt, response.response)
    insert_history_time = time.time() - start_time

    return response, response_time, context_time, chat_history_time, insert_history_time
        
async def ask_file(organization_id: str, session_id: str, user_id: str, prompt: str, file: UploadFile, rag: bool = True) -> str:
    file_extension = file.filename.split(".")[-1]

    if file_extension in agent.get_accepted_files():
        file_content = _read_file(file)
        
        prompt = f"""
            Prompt: {prompt}
            File content: {file_content}
        """
        
        return await ask(organization_id=organization_id, user_id=user_id, session_id=session_id, prompt=prompt, rag=rag)
    else:
        raise RuntimeError("File not accepted")
    
def _read_file(file: UploadFile) -> str:
    file_extension = file.filename.split(".")[-1]
    file_content = ""
    if file_extension == "pdf":
        reader = PdfReader(file.file)
        for page in reader.pages:
            file_content += page.extract_text()
    elif file_extension == "docx":
        document = Document(file.file)
        for para in document.paragraphs:
            file_content += para.text + "\n"
    elif file_extension == "txt":
        file_content = file.file.read()
    elif file_extension == "csv":
        file_content = pd.read_csv(file.file).to_string(index=False)
    elif file_extension == "xlsx":
        file_content = pd.read_excel(file.file).to_string(index=False)
    else:
        raise RuntimeError("File not currently supported for this agent")

    return file_content
