# Main entry point for Hugging Face Spaces
from app.main import app

# This file is used by Hugging Face Spaces to run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=7860)
