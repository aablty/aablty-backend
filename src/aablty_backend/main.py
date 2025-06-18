from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer

from .routes import projects, skills, facts, education, certifications, public, cv
from .db import init_db
from .config import settings
from .utils import ensure_upload_dir

# Init db and upload directory
init_db()
ensure_upload_dir()

# Configure security scheme
security = HTTPBearer()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="aablty Backend API",
    openapi_tags=[
        {
            "name": "projects",
            "description": "Endpoints for projects"
        },
        {
            "name": "skills",
            "description": "Endpoints for skills"
        },
        {
            "name": "facts",
            "description": "Endpoints for facts"
        },
        {
            "name": "education",
            "description": "Endpoints for education"
        },
        {
            "name": "certifications",
            "description": "Endpoints for certifications"
        },
        {
            "name": "cv",
            "description": "Endpoints for CV file"
        }
    ]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    public.router, prefix="/api", tags=["public"]
)
app.include_router(
    projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(
    skills.router, prefix="/api/skills", tags=["skills"])
app.include_router(
    facts.router, prefix="/api/facts", tags=["facts"])
app.include_router(
    education.router, prefix="/api/education", tags=["education"])
app.include_router(certifications.router,
                   prefix="/api/certifications", tags=["certifications"])
app.include_router(
    cv.router, prefix="/api/cv", tags=["cv"])

# Mount static files
app.mount(
    "/static", StaticFiles(directory="src/aablty_backend/static"), name="static")



@app.get("/")
async def root():
    return {
        "message": "aablty Backend API",
        "version": settings.VERSION,
        "docs": "/docs",
        "api": "/api/",
    }
