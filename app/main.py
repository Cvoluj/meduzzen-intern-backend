from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from app.routers import health
from app.config.app_config import server_setting
from redis import asyncio as aioredis
from app.db.database import AsyncSession, get_db


app = FastAPI()
app.include_router(health.router)


origins = [
    f'http://localhost:{server_setting.PORT}'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["*"],
)

@app.on_event('startup')
async def startup_event():
    redis = aioredis.from_url(f'redis://{server_setting.REDIS_HOST}', encoding='utf8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')

@app.get("/get_db")
async def some_endpoint(db: AsyncSession = Depends(get_db)):
    
    return {"message": "Data retrieved from the database"}