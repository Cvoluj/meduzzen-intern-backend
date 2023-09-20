from fastapi import FastAPI
import uvicorn
from routers import health
from core.config import ServerSettings

app = FastAPI()
config = ServerSettings()
app.include_router(health.router)

host = config.HOST
port = config.PORT
reload = config.RELOAD
log_level = config.LOG_LEVEL



