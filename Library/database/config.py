import os
from sqlalchemy.orm import declarative_base,sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

_RAW_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/library_db")
if _RAW_DATABASE_URL.startswith("postgresql://") and "+asyncpg" not in _RAW_DATABASE_URL:
    DATABASE_URL = _RAW_DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
else:
    DATABASE_URL = _RAW_DATABASE_URL

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 *24

FINE_PER_DAY = float(os.getenv("FINE_PER_DAY", "1.0"))

Base = declarative_base()

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
