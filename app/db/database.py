from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import URL, text
from app.config.app_config import server_setting
import asyncio


engine = create_async_engine(
    url=server_setting.DB_URL,
    echo=True
)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

async def test_database_connection():
    try:
        async with async_session() as session:
            result = await session.execute(text('SELECT 1'))
            print(result)
            return "Database connection is successful"
    except Exception as e:
        return f"Database connection error: {str(e)}"

if __name__ == "__main__":
    result = asyncio.run(test_database_connection())
    print(result)