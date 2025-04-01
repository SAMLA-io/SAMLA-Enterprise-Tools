# Written by Juan Pablo Gutiérrez

from fastapi import APIRouter, HTTPException
from ..helpers.chat_recommendations import get_chat_recommendations

router = APIRouter()

@router.get("/get_chat_recommendations")
async def get_chat_recommendations_route(organization_id: str, user_id: str, session_id: str):
    """ 
    This function is used to get the recommendations based on the chat.
    """ 

    try:
        response, response_time, context_time, chat_history_time, insert_history_time = await get_chat_recommendations(organization_id, user_id, session_id)
        
        return {
            "message": response,
            "response_time": response_time,
            "context_time": context_time,
            "chat_history_time": chat_history_time,
            "insert_history_time": insert_history_time
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

