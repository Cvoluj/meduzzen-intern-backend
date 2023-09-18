from fastapi import FastAPI
import uvicorn
from routers import health
from dotenv import load_dotenv
import os


load_dotenv()
HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))


app = FastAPI()
app.include_router(health.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, log_level="info", reload=os.getenv('DEBUG', False))
