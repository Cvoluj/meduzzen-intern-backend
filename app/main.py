from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import health
from app.config.app_config import ServerSettings


app = FastAPI()
config = ServerSettings()
app.include_router(health.router)


host = config.HOST
port = config.PORT
reload = config.RELOAD
log_level = config.LOG_LEVEL

origins = [
    f'http://localhost:{port}'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET" "POST" "OPTIONS" "DELETE" "PATCH" "PUT"],
    allow_headers=["*"],
)




