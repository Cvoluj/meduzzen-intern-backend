from fastapi import FastAPI
import uvicorn
from routers import health
from core.config import ServerSettings

app = FastAPI()
config = ServerSettings()
app.include_router(health.router)


if __name__ == "__main__":
    host = config.HOST
    port = config.PORT
    reload = config.RELOAD
    log_level = config.LOG_LEVEL
    uvicorn.run("main:app", host=host, port=port, log_level=log_level, reload=reload)
