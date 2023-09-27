from fastapi import APIRouter, Depends
from sqlalchemy import text
from redis import asyncio as aioredis
from app.db.database import get_db, AsyncSession, get_redis



router = APIRouter()

@router.get('/')
async def health_check():
    return {
        'status_code': 200,
        'detail': 'ok',
        'result': 'working'
    }

@router.get("/check_db")
async def check_db_connection(db: AsyncSession = Depends(get_db)):    
    try:
        async with db.begin() as conn:
            result = await conn.session.execute(text('SELECT 1'))
            return "Database connection is successful"
    except Exception as e:
        return f"Database connection error: {str(e)}"

@router.get("/check_redis")
async def check_redis_connection(redis: aioredis.Redis = Depends(get_redis)):
    try:
        result = await redis.ping()
        if result == True:
            return "Redis connection is successful"
        else:
            return "Redis connection is not successful"
    except Exception as e:
        return f"Redis connection error: {str(e)}"
