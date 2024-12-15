# Written by Juan Pablo Gutierrez

from fastapi import APIRouter

router = APIRouter()

@router.get("/redirect")
def redirect_assistant(message: str):
    """
    Redirects the user to an assistant based on the message and requirements.
    """
    return {"message": message}

