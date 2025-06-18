from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query
)
from sqlalchemy.orm import Session
from typing import List

from ..db import get_db
from ..schemas import (
    Certification,
    CreateCertification,
    CertificationStatus,
    Translation
)
from ..crud import (
    get_certifications,
    create_certification,
    delete_certification
)
from ..utils import convert_db_model_to_schema
from ..auth import AdminAuth


router = APIRouter()


@router.post("/")
def create_certification_endpoint(
    name_ru: str = Query(...),
    name_en: str = Query(...),
    provider_ru: str = Query(...),
    provider_en: str = Query(...),
    year: str = Query(...),
    status: CertificationStatus = Query(...),
    admin_auth: bool = AdminAuth,
    db: Session = Depends(get_db)
):
    education_status_translation = {
        CertificationStatus.CURRENT: Translation(ru="Текущий", en="Current"),
        CertificationStatus.COMPLETED: Translation(ru="Завершенный", en="Completed"),
    }
    certification = CreateCertification(
        name=Translation(ru=name_ru, en=name_en),
        provider=Translation(ru=provider_ru, en=provider_en),
        year=year,
        status=education_status_translation[status]
    )
    create_certification(db, certification)

    return {
        "success": True,
    }


@router.get("/", response_model=List[Certification])
def get_certifications_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):

    db_certifications = get_certifications(db, skip=skip, limit=limit)

    return [convert_db_model_to_schema(cert, Certification) for cert in db_certifications]


@router.delete("/{certification_id}")
def delete_certification_endpoint(
    certification_id: str,
    admin_auth: bool = AdminAuth,
    db: Session = Depends(get_db)
):

    success = delete_certification(db, certification_id)
    if not success:
        raise HTTPException(status_code=404, detail="Certification not found")

    return {
        "success": True
    }
