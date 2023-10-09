from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from app.routers import health, user_routers
from app.config.app_config import server_setting
from redis import asyncio as aioredis



app = FastAPI()
app.include_router(health.router)
app.include_router(user_routers.user_endpoints)

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