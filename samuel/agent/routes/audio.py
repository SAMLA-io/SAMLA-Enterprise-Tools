from fastapi import APIRouter, File, UploadFile
from ..helpers.audio_processing import get_audio_processing

router = APIRouter()

@router.post("/audio")
async def upload_file_route(company_id: str, file: UploadFile = File(...)):
    return get_audio_processing(company_id, file)