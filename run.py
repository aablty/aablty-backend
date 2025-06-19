import os
import uvicorn
from fastapi.staticfiles import StaticFiles
from src.aablty_backend.main import app


if os.getenv("RENDER"):
    static_path = "/opt/render/project/data/static"
    os.makedirs(static_path, exist_ok=True)
else:
    static_path = "src/aablty_backend/static"
# Mount the static files directory
app.mount("/static", StaticFiles(directory=static_path), name="static")

if __name__ == "__main__":
    uvicorn.run(
        "src.aablty_backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
