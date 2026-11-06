import uuid
from pathlib import Path
from typing import List
from fastapi import UploadFile

UPLOAD_DIR = Path("uploads")


async def save_file(file: UploadFile, folder: str = "") -> str:
    clean_folder = folder.strip("/ ") if folder else ""
    target_dir = UPLOAD_DIR / clean_folder if clean_folder else UPLOAD_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    original_filename = file.filename or "file.jpg"
    if "." in original_filename:
        ext = original_filename.rsplit(".", 1)[-1].lower()
    else:
        ext = "jpg"

    new_filename = f"{uuid.uuid4()}.{ext}"
    path = target_dir / new_filename

    content = await file.read()
    path.write_bytes(content)

    return f"{clean_folder}/{new_filename}" if clean_folder else new_filename


async def save_files(files: List[UploadFile], folder: str = "") -> List[str]:
    saved = []
    for file in files:
        saved_path = await save_file(file, folder)
        saved.append(saved_path)
    return saved


async def save_teacher_photo(file: UploadFile) -> str:
    return await save_file(file, "teachers")
