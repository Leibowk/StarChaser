from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings

DATABASE_URL = (
    f"postgresql+psycopg2://{settings.POSTGRES.USER}:"
    f"{settings.POSTGRES.PASSWORD}@{settings.POSTGRES.HOST}:"
    f"{settings.POSTGRES.PORT}/{settings.POSTGRES.DB}"
)

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()