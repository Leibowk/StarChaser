from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.POSTGRES.USER}:"
    f"{settings.POSTGRES.PASSWORD}@{settings.POSTGRES.HOST}:"
    f"{settings.POSTGRES.PORT}/{settings.POSTGRES.DB}"
)

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()