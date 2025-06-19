import os

from cloudinary import uploader, api, exceptions
from fastapi import UploadFile, HTTPException
from fastapi.concurrency import run_in_threadpool

from .config import settings


ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE = settings.MAX_FILE_SIZE


def is_allowed_file(filename: str) -> bool:
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS


async def upload_file(upload_file: UploadFile) -> dict:
    # Validate file
    if not upload_file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    if not is_allowed_file(upload_file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # Check file size
    content = await upload_file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large")

    def upload_to_cloudinary():
        return uploader.upload(
            content
        )

    result = await run_in_threadpool(upload_to_cloudinary)

    if not result:
        raise HTTPException(status_code=500, detail="Image upload failed")

    return result


async def delete_file(image_public_id: str) -> bool:
    if not image_public_id:
        return False

    def delete_from_cloudinary():
        return uploader.destroy(image_public_id)

    try:
        result = await run_in_threadpool(delete_from_cloudinary)
        return result.get("result") == "ok"
    except Exception:
        return False


def upload_cv(content: bytes, public_id) -> str:
    result = uploader.upload(
        content,
        resource_type="raw",
        public_id=public_id,
        overwrite=True,
        format="pdf"
    )
    return result["secure_url"]


def get_cv_info(public_id) -> dict:
    try:
        result = api.resource(
            public_id,
            resource_type="raw"
        )
        return {
            "exists": True,
            "download_url": result["secure_url"]
        }
    except exceptions.NotFound:
        return {
            "exists": False,
            "message": "CV not available"
        }


def convert_db_model_to_schema(db_model, schema_class):
    # Handle Fact model
    if hasattr(db_model, 'content_ru') and hasattr(db_model, 'content_en') and not hasattr(db_model, 'title_ru'):
        data = {
            "id": db_model.id,
            "content": {
                "ru": db_model.content_ru,
                "en": db_model.content_en
            }
        }
        return schema_class(**data)

    # Handle models with title translation (Project, Skills)
    elif hasattr(db_model, 'title_ru') and hasattr(db_model, 'title_en'):
        data = {
            "id": db_model.id,
            "title": {
                "ru": db_model.title_ru,
                "en": db_model.title_en
            }
        }

        # Add description for Project
        if hasattr(db_model, 'description_ru') and hasattr(db_model, 'description_en'):
            data["description"] = {
                "ru": db_model.description_ru,
                "en": db_model.description_en
            }

        # Add specific fields
        for field in ['image', 'links', 'items', 'stack', 'type', 'image_public_id']:
            if hasattr(db_model, field):
                data[field] = getattr(db_model, field)

        return schema_class(**data)

    # Handle Education model
    elif hasattr(db_model, 'institution_ru'):
        data = {
            "id": db_model.id,
            "institution": {
                "ru": db_model.institution_ru,
                "en": db_model.institution_en,
            },
            "degree": {
                "ru": db_model.degree_ru,
                "en": db_model.degree_en
            },
            "start_year": db_model.start_year,
            "end_year": db_model.end_year,
            "status": {
                "ru": db_model.status_ru,
                "en": db_model.status_en
            },
            "location": {
                "ru": db_model.location_ru,
                "en": db_model.location_en
            }
        }
        return schema_class(**data)

    # Handle Certification model
    elif hasattr(db_model, 'name_ru'):
        data = {
            "id": db_model.id,
            "name": {
                "ru": db_model.name_ru,
                "en": db_model.name_en
            },
            "provider": {
                "ru": db_model.provider_ru,
                "en": db_model.provider_en
            },
            "year": db_model.year,
            "status": {
                "ru": db_model.status_ru,
                "en": db_model.status_en
            }
        }
        return schema_class(**data)

    raise ValueError(
        f"Unable to convert model {type(db_model)} to schema {schema_class}")
