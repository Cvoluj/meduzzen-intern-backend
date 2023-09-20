from fastapi import FastAPI
from app.routers import health
from app.core.config import ServerSettings

app = FastAPI()
config = ServerSettings()
app.include_router(health.router)

host = config.HOST
port = config.PORT
reload = config.RELOAD
log_level = config.LOG_LEVEL



