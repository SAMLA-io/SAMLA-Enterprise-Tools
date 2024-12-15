# Written by Juan Pablo Gutiérrez

from fastapi import APIRouter, File, UploadFile

router = APIRouter()

@router.post("/input")
def input_message(message: str):
    """ 
    This function is used to send a message to Samuel.
    """
    return {"message": message}

@router.post("/output")
def output_message(message: str):
    """ 
    This function is used to send a message back to the user from Samuel.
    """
    return {"message": message}

@router.post("/upload")
def upload_file(file: UploadFile = File(...)):
    """ 
    This function is used to upload a file to the server for Samuel to process.
    """
    return {"filename": file.filename}
