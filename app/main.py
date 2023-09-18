from fastapi import FastAPI
import uvicorn
from routers import health
from core.config import ServerSettings

app = FastAPI()
config = ServerSettings().model_dump()



app.include_router(health.router)


if __name__ == "__main__":
    host = config['HOST']
    port = config['PORT']
    reload = config['RELOAD']
    uvicorn.run("main:app", host=host, port=port, log_level="info", reload=reload)
