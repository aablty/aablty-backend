import uvicorn
from fastapi.staticfiles import StaticFiles
from src.aablty_backend.main import app

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(
        "src.aablty_backend.main:app",
        host="localhost",
        port=8000,
        reload=True
    )
