# Written by Juan Pablo Gutiérrez

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class DataModel(BaseModel):
    """ 
    This class defines the data model for the graphs.
    """
    x: list[float]
    y: list[float]


@router.get("/get_graphs")
def get_graphs(data: DataModel):
    """ 
    This function is used to get the graphs based on the data.
    """
    return {"message": "Graphs"}
