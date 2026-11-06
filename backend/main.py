from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.app.auth.router import router as auth
from backend.app.owner.router import router as owner
from backend.app.upload.router import router as upload

app = FastAPI(title="Texnikum API")

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://192.168.1.105:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https?://.*\.ngrok(-free)?\.(app|dev)",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth)
app.include_router(owner)
app.include_router(upload)

# Ensure upload directories exist
uploads_dir = Path("uploads")
uploads_dir.mkdir(parents=True, exist_ok=True)
for sub in ["teachers", "news", "deficiency"]:
    (uploads_dir / sub).mkdir(parents=True, exist_ok=True)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/health")
def health_check():
    return {"status": "ok"}
