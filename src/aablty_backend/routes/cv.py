from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os

from ..db import get_db
from ..auth import AdminAuth
from ..utils import (
    upload_cv,
    get_cv_info
)

router = APIRouter()

CV_PUBLIC_ID = "cv/cv"
CV_FOLDER = "cv"


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

        content = await cv_file.read()

        url = upload_cv(content, CV_PUBLIC_ID)

        return {
            "detail": "CV uploaded successfully",
            "download_url": url
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info")
async def get_cv_info_public():
    try:
        info = get_cv_info(CV_PUBLIC_ID)
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
