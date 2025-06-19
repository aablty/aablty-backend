import json
from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Query
)
from sqlalchemy.orm import Session

from ..db import get_db
from ..schemas import (
    CreateProject,
    Project,
    ProjectLink,
    ProjectType,
    Translation
)
from ..crud import (
    get_project,
    get_projects,
    create_project,
    delete_project
)
from ..utils import (
    upload_file,
    delete_file,
    convert_db_model_to_schema
)
from ..auth import AdminAuth

router = APIRouter()


@router.post("/")
async def create_project_endpoint(
    type: ProjectType = Query(...),
    title_ru: str = Query(...),
    title_en: str = Query(...),
    description_ru: str = Query(...),
    description_en: str = Query(...),
    image: UploadFile = File(...),
    stack: List[str] = Query(..., description='FastAPI, React'),
    links: List[str] = Query(...,
                             description='{"label": "text", "link": "url"}'),
    admin_auth: bool = AdminAuth,
    db: Session = Depends(get_db)
):
    try:
        try:
            links_list = [json.loads(link) for link in links]

        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=400, detail=f"Invalid JSON in stack or links: {str(e)}")

        # Handle image upload if provided
        if image and image.filename:
            upload_image = await upload_file(image)
            print(upload_image)

        project = CreateProject(
            title=Translation(ru=title_ru, en=title_en),
            description=Translation(ru=description_ru, en=description_en),
            stack=stack,
            type=type,
            image=upload_image["secure_url"],
            image_public_id=upload_image["public_id"],
            links=[ProjectLink(**link) for link in links_list]
        )

        create_project(db, project)

        return {
            "success": True
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[Project])
def get_projects_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    db_projects = get_projects(db, skip=skip, limit=limit)
    
    return [convert_db_model_to_schema(proj, Project) for proj in db_projects]


@router.delete("/{project_id}")
async def delete_project_endpoint(
    project_id: str,
    admin_auth: bool = AdminAuth,
    db: Session = Depends(get_db)
):
    # Get project to check if image needs to be deleted
    db_project = get_project(db, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Delete image file if exists
    if db_project.image_public_id:
        await delete_file(db_project.image_public_id)

    # Delete project from DB
    success = delete_project(db, project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")

    return {"success": True}
