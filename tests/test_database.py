from app.db.database import async_session
from sqlalchemy import text
import pytest


@pytest.mark.asyncio
async def test_database_connection():
    try:
        async with async_session() as session:
            result = await session.execute(text('SELECT 1'))
            return "Database connection is successful"
    except Exception as e:
        return f"Database connection error: {str(e)}"