# Written by Juan Pablo Gutiérrez

from fastapi import APIRouter
from pydantic import BaseModel
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

router = APIRouter()

@router.get("/get_graphs")
def get_graphs_route(x: list[float], y: list[float]):
    """ 
    This function is used to get the graphs based on the data.
    """
    plt.figure()
    plt.plot(x, y)
    plt.title("Graph from Data")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    graph_png = base64.b64encode(buf.getvalue()).decode('utf-8')

    return {"message": "Graphs", "graph": graph_png}