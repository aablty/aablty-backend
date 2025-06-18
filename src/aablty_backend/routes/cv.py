from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os

from ..db import get_db
from ..auth import AdminAuth

router = APIRouter()

CV_FILE_PATH = "src/aablty_backend/static/cv"

def ensure_cv_dir():
    os.makedirs(CV_FILE_PATH, exist_ok=True)

def get_current_cv_file():
    ensure_cv_dir()
    
    if os.path.exists(CV_FILE_PATH):
        files = os.listdir(CV_FILE_PATH)
        if files:
            return os.path.join(CV_FILE_PATH, files[0])
    return None

def delete_current_cv():
    ensure_cv_dir()
    
    if os.path.exists(CV_FILE_PATH):
        files = os.listdir(CV_FILE_PATH)
        for file in files:
            file_path = os.path.join(CV_FILE_PATH, file)
            try:
                os.remove(file_path)
                print(f"Удалён старый CV: {file}")
            except Exception as e:
                print(f"Ошибка удаления CV: {e}")

@router.post("/upload")
async def upload_cv_endpoint(
    cv_file: UploadFile = File(...),
    admin_auth: bool = AdminAuth,
    db: Session = Depends(get_db)
):
    try:
        # Проверяем тип файла (только PDF)
        if not cv_file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400, 
                detail="Only PDF files are allowed for CV"
            )
        
        delete_current_cv()
        
        ensure_cv_dir()
        cv_path = os.path.join(CV_FILE_PATH, "cv.pdf")
        
        with open(cv_path, "wb") as buffer:
            content = await cv_file.read()
            buffer.write(content)
        
        return {
            "detail": "CV uploaded successfully",
            "filename": "cv.pdf",
            "download_url": "/cv/download"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download")
async def download_cv_public():
    try:
        cv_path = "src/aablty_backend/static/cv/cv.pdf"

        if not os.path.exists(cv_path):
            raise HTTPException(
                status_code=404,
                detail="CV file not found"
            )

        return FileResponse(
            path=cv_path,
            filename="cv.pdf",
            media_type="application/pdf"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info")
async def get_cv_info_public():
    try:
        cv_path = "src/aablty_backend/static/cv/cv.pdf"

        if not os.path.exists(cv_path):
            return {
                "exists": False,
                "message": "CV not available"
            }

        # Получаем размер файла
        file_stats = os.stat(cv_path)
        file_size = file_stats.st_size

        return {
            "exists": True,
            "filename": "cv.pdf",
            "size_mb": round(file_size / (1024 * 1024), 2),
            "download_url": "/api/cv/download"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
