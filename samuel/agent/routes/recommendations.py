# Written by Juan Pablo Gutiérrez

from fastapi import APIRouter
from ..helpers.chat_recommendations import get_chat_recommendations

router = APIRouter()

@router.get("/get_chat_recommendations")
def get_chat_recommendations_route(company_id: str):
    """ 
    This function is used to get the recommendations based on the chat.
    """ 
    try:
        response = get_chat_recommendations(company_id)
        return {
            "statusCode": 200,
            "message": response
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "message": str(e)
        }

