from fastapi import APIRouter

router = APIRouter()

@router.get("/get_person")
def get_person(person_id: str):
    """
    Retrieve a person's information from the directory.
    """
    return {"message": "Person information retrieved"}

@router.post("/add_person")
def add_person(person: dict):
    """
    Add a person to the directory.
    """
    return {"message": "Person added"}

@router.post("/search")
def search(query: str):
    """
    Perform a semantic search based on the query.
    """
    return {"message": "Search results"}