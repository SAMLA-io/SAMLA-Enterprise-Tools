# Written by Juan Pablo Gutiérrez

from fastapi import APIRouter, HTTPException
from ..helpers.chat_recommendations import get_chat_recommendations

router = APIRouter()

@router.get("/get_chat_recommendations")
async def get_chat_recommendations_route(company_id: str, user_id: str, session_id: str):
    """ 
    This function is used to get the recommendations based on the chat.
    """ 

    try:
        response = await get_chat_recommendations(company_id, user_id, session_id)
        return {
            "message": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

