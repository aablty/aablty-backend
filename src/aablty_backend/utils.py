import os
import uuid
import aiofiles
from fastapi import UploadFile, HTTPException
from PIL import Image
import io

from .config import settings


UPLOAD_DIR = "src/aablty_backend/static/images"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE = settings.MAX_FILE_SIZE


def ensure_upload_dir():
    os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_file_extension(filename: str) -> str:
    return os.path.splitext(filename)[1].lower()


def is_allowed_file(filename: str) -> bool:
    return get_file_extension(filename) in ALLOWED_EXTENSIONS


def generate_unique_filename(original_filename: str) -> str:
    extension = get_file_extension(original_filename)
    unique_id = str(uuid.uuid4())
    return f"{unique_id}{extension}"


async def save_upload_file(upload_file: UploadFile) -> str:
    ensure_upload_dir()

    # Validate file
    if not upload_file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    if not is_allowed_file(upload_file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # Read file content
    content = await upload_file.read()

    # Check file size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large")

    # Validate image
    try:
        image = Image.open(io.BytesIO(content))
        image.verify()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")

    # Generate unique filename
    filename = generate_unique_filename(upload_file.filename)
    file_path = os.path.join(UPLOAD_DIR, filename)
    print(file_path)

    # Save file
    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(content)

    # Return relative path for frontend
    return f"/static/images/{filename}"


def delete_file(file_path: str) -> bool:
    if not file_path or not file_path.startswith("/static/images/"):
        return False

    # Convert to actual file path
    filename = file_path.replace("/static/images/", "")
    actual_path = os.path.join(UPLOAD_DIR, filename)

    try:
        if os.path.exists(actual_path):
            os.remove(actual_path)
            return True
    except Exception:
        pass

    return False


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
        for field in ['image', 'links', 'items', 'stack', 'type']:
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
