# Written by Juan Pablo Gutiérrez

from fastapi import APIRouter
from pydantic import BaseModel
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

router = APIRouter()

@router.get("/get_graphs")
def get_graphs_route(x: str, y: str):
    """ 
    This function is used to get the graphs based on the data.
    x and y can be comma-separated values, e.g. "1,2,3,4,5" or JSON-like arrays "[1,2,3,4,5]"
    """
    # Clean input: remove brackets if present
    x = x.strip("[]")
    y = y.strip("[]")
    
    # Convert comma-separated strings to lists of floats
    x_values = [float(val) for val in x.split(",")]
    y_values = [float(val) for val in y.split(",")]
    
    plt.figure()
    plt.plot(x_values, y_values)
    plt.title("Graph from Data")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    graph_png = base64.b64encode(buf.getvalue()).decode('utf-8')

    return {"message": "Graphs", "graph": graph_png}