import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        "src.aablty_backend.main:app",
        host="localhost",
        port=8000,
        reload=True
    )
