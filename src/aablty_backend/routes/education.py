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
    Education,
    CreateEducation,
    EducationStatus,
    Translation
)
from ..crud import (
    get_educations,
    create_education,
    delete_education
)
from ..utils import convert_db_model_to_schema
from ..auth import AdminAuth

router = APIRouter()


@router.post("/")
def create_education_endpoint(
    institution_ru: str = Query(...),
    institution_en: str = Query(...),
    degree_ru: str = Query(...),
    degree_en: str = Query(...),
    start_year: str = Query(...),
    end_year: str = Query(...),
    status: EducationStatus = Query(...),
    location_ru: str = Query(...),
    location_en: str = Query(...),
    admin_auth: bool = AdminAuth,
    db: Session = Depends(get_db)
):
    education_status_translation = {
        EducationStatus.CURRENT: Translation(ru="Текущий", en="Current"),
        EducationStatus.GRADUATED: Translation(ru="Закончил", en="Graduated"),
    }

    education = CreateEducation(
        institution=Translation(ru=institution_ru, en=institution_en),
        degree=Translation(ru=degree_ru, en=degree_en),
        start_year=start_year,
        end_year=end_year,
        status=education_status_translation[status],
        location=Translation(ru=location_ru, en=location_en)
    )
    create_education(db, education)

    return {
        "success": True,
    }


@router.get("/", response_model=List[Education])
def get_educations_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):

    db_educations = get_educations(db, skip=skip, limit=limit)

    return [convert_db_model_to_schema(edu, Education) for edu in db_educations]


@router.delete("/{education_id}")
def delete_education_endpoint(
    education_id: str,
    admin_auth: bool = AdminAuth,
    db: Session = Depends(get_db)
):

    success = delete_education(db, education_id)
    if not success:
        raise HTTPException(
            status_code=404, detail="Education record not found")

    return {
        "success": True,
    }
