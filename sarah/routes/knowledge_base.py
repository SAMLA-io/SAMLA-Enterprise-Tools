from fastapi import APIRouter

router = APIRouter()

@router.post("/add_document")
def add_document(document: dict):
    """
    Add a document to the knowledge base.
    """
    return {"message": "Document added"}

@router.get("/get_document")
def get_document(doc_id: str):
    """
    Retrieve a document from the knowledge base.
    """
    return {"message": "Document retrieved"}