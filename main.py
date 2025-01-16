import uvicorn
import logging
from fastapi import FastAPI

from dotenv import load_dotenv

load_dotenv()

from app.api.v1.endpoints.chat_workflow import router as chat_router

# Configure logging
logging.basicConfig(
    filename='app.log',  # Log file name
    level=logging.INFO,  # Log level
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
)

app = FastAPI(
    title="text-2-SQL API",
    description="An API for chat-based question answering using text-2-SQL workflow",
    version="1.0.0",
)

app.include_router(chat_router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
