from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import URL, text
from app.config.app_config import server_setting
import asyncio


engine = create_async_engine(
    url=server_setting.DB_URL,
    echo=True
)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
