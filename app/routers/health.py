from fastapi import APIRouter
from app.db.database import async_session
from sqlalchemy import text
from redis import asyncio as aioredis



router = APIRouter()

@router.get('/')
async def health_check():
    return {
        'status_code': 200,
        'detail': 'ok',
        'result': 'working'
    }

@router.get("/check_db")
async def check_db_connection():    
    try:
        async with async_session() as session:
            result = await session.execute(text('SELECT 1'))
            return "Database connection is successful"
    except Exception as e:
        return f"Database connection error: {str(e)}"

@router.get('/check_redis')
async def check_redis_connection():
    pool = aioredis.ConnectionPool(
        host='redis',  
        port=6379,     
        encoding='utf8',
        decode_responses=True)
    redis = aioredis.Redis(connection_pool=pool)
    
    return await redis.ping()
