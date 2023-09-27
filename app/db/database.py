from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.config.app_config import server_setting
from redis import asyncio as aioredis


engine = create_async_engine(
    url=server_setting.DB_URL,
    echo=True
)

async def get_db():
    async with AsyncSession(engine) as db:
        yield db

redis_pool= None 
async def get_redis():
    global redis_pool
    if not redis_pool:
        redis_pool = await aioredis.from_url(f'redis://redis', encoding='utf8', decode_responses=True)

    return redis_pool