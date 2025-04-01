from fastapi import APIRouter, File, UploadFile
from ..helpers.audio_processing import get_audio_processing

router = APIRouter()

@router.post("/audio")
async def upload_file_route(organization_id: str, session_id: str, user_id: str, file: UploadFile = File(...)):
    return await get_audio_processing(organization_id, session_id, user_id, file)