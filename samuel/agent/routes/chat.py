# Written by Juan Pablo Gutiérrez

from fastapi import APIRouter, File, UploadFile
from ..helpers.prompting import ask, ask_file
from ..setup import agent
router = APIRouter()

@router.get("/input")
def input_message_route(company_id: str, message: str):
    """ 
    This function is used to send a message to the Agent.
    """
    try:
        response = ask(company_id, message, agent.get_rag())
        return {
            "statusCode": 200,
            "message": response
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "message": str(e)
        }

@router.post("/upload")
async def upload_file_route(company_id: str, message: str, file: UploadFile = File(...)):
    """ 
    This function is used to upload a file to the server for the Agent to process.
    """
    try:
        response = ask_file(company_id, message, file, agent.get_rag())
        return {
            "statusCode": 200,
            "message": response
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "message": str(e)
        }