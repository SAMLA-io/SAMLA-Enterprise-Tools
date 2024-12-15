# Written by Juan Pablo Gutiérrez

from fastapi import APIRouter

router = APIRouter()

@router.get("/start_monitor ")
def start_monitor():
    """ 
    This function is used to start the monitor.
    """
    return {"message": "Monitor started"}

@router.get("/stop_monitor")
def stop_monitor():
    """ 
    This function is used to stop the monitor.
    """
    return {"message": "Monitor stopped"}

@router.get("/get_status")
def get_status():
    """ 
    This function is used to get the status of the monitor.
    """
    return {"message": "Monitor status"}

@router.get("/get_latest")
def get_latest():
    """ 
    This function is used to get the latest data of the monitor.
    """
    return {"message": "Monitor data"}
