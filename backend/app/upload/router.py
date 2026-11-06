from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from backend.app.upload.servise import save_files, save_teacher_photo
from backend.depensies import get_current_user

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("")
@router.post("/")
async def upload_files(
    folder: str = Form(""),
    files: Optional[List[UploadFile]] = File(None),
    file: Optional[UploadFile] = File(None),
    current_user = Depends(get_current_user),
):
    upload_list: List[UploadFile] = []
    if files:
        upload_list.extend(files)
    if file:
        upload_list.append(file)

    if not upload_list:
        raise HTTPException(status_code=400, detail="Fayl yuklanmadi")

    saved_files = await save_files(upload_list, folder)
    return {
        "files": saved_files,
        "url": saved_files[0] if saved_files else None,
    }


@router.post("/teacher-photo")
async def upload_teacher_photo(
    file: UploadFile = File(...),
):
    photo_url = await save_teacher_photo(file)

    return {
        "url": photo_url
    }
