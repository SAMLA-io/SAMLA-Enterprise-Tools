# Written by Juan Pablo Gutiérrez

from fastapi import APIRouter, File, UploadFile, HTTPException
from ..helpers.prompting import ask, ask_file
from ..setup import agent
router = APIRouter()

@router.get("/input")
async def input_message_route(organization_id: str, session_id: str, user_id: str, message: str):
    """ 
    This function is used to send a message to the Agent.

    Args:
        organization_id: str
        session_id: str
        user_id: str
        message: str
    
    Returns:
        response: str
        response_time: float
        context_time: float
        chat_history_time: float
        insert_history_time: float
    """
    try:
        response, response_time, context_time, chat_history_time, insert_history_time = await ask(organization_id=organization_id, user_id=user_id, session_id=session_id, prompt=message, rag=agent.get_rag())
        return {
            "message": response,
            "context_time": context_time,
            "chat_history_time": chat_history_time,
            "response_time": response_time,
            "insert_history_time": insert_history_time
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload")
async def upload_file_route(organization_id: str, session_id: str, user_id: str, message: str, file: UploadFile = File(...)):
    """
    This function is used to upload a file to the server for the Agent to process.

    Args:
        organization_id: str
        session_id: str
        user_id: str
        message: str
        file: UploadFile
    
    Returns:
        response: str
        response_time: float
        context_time: float
        chat_history_time: float
        insert_history_time: float
    """
    try:
        response, response_time, context_time, chat_history_time, insert_history_time = await ask_file(organization_id=organization_id, session_id=session_id, user_id=user_id, prompt=message, file=file, rag=agent.get_rag())
        return {
            "message": response,
            "response_time": response_time,
            "context_time": context_time,
            "chat_history_time": chat_history_time,
            "insert_history_time": insert_history_time
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))