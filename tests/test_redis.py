import pytest
from app.main import FastAPICache, RedisBackend
from redis import asyncio as aioredis
from app.config.app_config import server_setting


@pytest.mark.asyncio
async def test_redis_backend():
    # Initialize Redis for testing
    redis = aioredis.from_url(f'redis://{server_setting.REDIS_HOST}', encoding='utf8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')
    yield FastAPICache