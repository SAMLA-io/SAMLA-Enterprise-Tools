from fastapi import APIRouter, File, UploadFile, HTTPException
from ..helpers.audio_processing import get_audio_processing

router = APIRouter()

@router.post("/audio")
async def upload_file_route(organization_id: str, session_id: str, user_id: str, file: UploadFile = File(...)):
    """
    This function is used to upload a file to the server for the Agent to process.
    
    Args:
        organization_id: str
        session_id: str
        user_id: str
        file: UploadFile

    Returns:
        response: str
        response_time: float
        context_time: float
        chat_history_time: float
        insert_history_time: float
    """
    try:
        response, response_time, context_time, chat_history_time, insert_history_time = await get_audio_processing(organization_id, session_id, user_id, file)
        return {
            "message": response,
            "response_time": response_time,
            "context_time": context_time,
            "chat_history_time": chat_history_time,
            "insert_history_time": insert_history_time
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))