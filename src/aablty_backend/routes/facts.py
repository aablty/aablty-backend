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
    Fact,
    CreateFact,
    Translation
)
from ..crud import (
    get_facts,
    create_fact,
    delete_fact
)
from ..utils import convert_db_model_to_schema
from ..auth import AdminAuth

router = APIRouter()


@router.post("/", response_model=Fact)
def create_fact_endpoint(
    content_ru: str = Query(...),
    content_en: str = Query(...),
    admin_auth: bool = AdminAuth,
    db: Session = Depends(get_db)
):

    fact = CreateFact(
        content=Translation(
            ru=content_ru,
            en=content_en
        )
    )

    create_fact(db, fact)

    return {
        "success": True
    }


@router.get("/", response_model=List[Fact])
def get_facts_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    db_facts = get_facts(db, skip=skip, limit=limit)
    
    return [convert_db_model_to_schema(fact, Fact) for fact in db_facts]


@router.delete("/{fact_id}")
def delete_fact_endpoint(
    fact_id: str,
    admin_auth: bool = AdminAuth,
    db: Session = Depends(get_db)
):
    success = delete_fact(db, fact_id)
    if not success:
        raise HTTPException(status_code=404, detail="Fact not found")
    
    return {
        "success": True
    }
