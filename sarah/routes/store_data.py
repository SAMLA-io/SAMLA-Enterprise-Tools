from fastapi import APIRouter

router = APIRouter()

@router.post("/store_data")
def store_data(data: dict):
    """
    Store important information in JSON format.
    """
    return {"message": "Data stored"}

@router.get("/retrieve_data")
def retrieve_data(data_id: str):
    """
    Retrieve stored information.
    """
    return {"message": "Data retrieved"}