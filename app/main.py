from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from app.routers import health
from app.config.app_config import server_setting
from redis import asyncio as aioredis
from app.db.database import async_session
from sqlalchemy import text


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
    global redis 
    redis = aioredis.from_url(f'redis://redis', encoding='utf8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')


@app.get("/check_db")
async def check_db_connection():    
    try:
        async with async_session() as session:
            result = await session.execute(text('SELECT 1'))
            return "Database connection is successful"
    except Exception as e:
        return f"Database connection error: {str(e)}"

@app.get('/check_redis')
async def check_redis_connection():
    result = await redis.ping()
    return result

