# Written by Juan Pablo Gutiérrez
# 23 01 2025

from agent.helpers.database_connection import get_chat_history, insert_chat_history
from ..setup import agent, execute_orchestrator
from fastapi import  UploadFile
from pypdf import PdfReader
from docx import Document
import pandas as pd
from ..helpers.rag_connection import get_rag_context

def ask(company_id: str, user_id: str, session_id: str, prompt: str, rag: bool = True, insert_history: bool = True) -> str:
    context = ""
    if rag:
        context = get_rag_context(company_id, prompt)

    chat_history = ""
    if session_id:
        chat_history = get_chat_history(company_id, user_id, session_id)

    new_prompt = f"Prompt: {prompt}\n"
    if context:
        new_prompt = f"Context: {context}\n" + new_prompt
    if chat_history:
        new_prompt = f"Chat history: {chat_history}\n" + new_prompt

    response = execute_orchestrator(new_prompt)

    if insert_history:
        insert_chat_history(company_id, session_id, user_id, prompt, response.response)

    return response
        
def ask_file(company_id: str, session_id: str, user_id: str, prompt: str, file: UploadFile, rag: bool = True) -> str:
    file_extension = file.filename.split(".")[-1]

    if file_extension in agent.get_accepted_files():
        file_content = _read_file(file)
        
        prompt = f"""
            Prompt: {prompt}
            File content: {file_content}
        """
        
        return ask(company_id=company_id, user_id=user_id, session_id=session_id, prompt=prompt, rag=rag)
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
