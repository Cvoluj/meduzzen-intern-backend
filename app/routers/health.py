from fastapi import APIRouter
from app.db.database import async_session
from sqlalchemy import text

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
