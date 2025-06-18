from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query
)
from sqlalchemy.orm import Session

from ..db import get_db
from ..schemas import (
    SkillCategory,
    CreateSkillCategory,
    Translation
)
from ..crud import (
    get_skills,
    create_skill_category,
    delete_skill_category
)
from ..utils import convert_db_model_to_schema
from ..auth import AdminAuth

router = APIRouter()


@router.post("/")
def create_skill_category_endpoint(
    title_ru: str = Query(...),
    title_en: str = Query(...),
    items: List[str] = Query(...),
    admin_auth: bool = AdminAuth,
    db: Session = Depends(get_db)
):
    try:
        skill_category = CreateSkillCategory(
            title=Translation(
                ru=title_ru,
                en=title_en
            ),
            items=items
        )
        create_skill_category(db, skill_category)

        return {
            "success": True
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[SkillCategory])
def get_skills_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    db_skill_categories = get_skills(db, skip=skip, limit=limit)

    return [convert_db_model_to_schema(cat, SkillCategory) for cat in db_skill_categories]


@router.delete("/{skill_category_id}")
def delete_skill_category_endpoint(
    skill_category_id: str,
    admin_auth: bool = AdminAuth,
    db: Session = Depends(get_db)
):
    success = delete_skill_category(db, skill_category_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Skill category not found")

    return {
        "success": True
    }
