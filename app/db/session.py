from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os
load_dotenv()

# Replace with your actual database URL
DATABASE_URL = os.getenv("database_url")

# Create engine
engine = create_async_engine(DATABASE_URL, echo=True, future=True)




# Create session factory
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)





# Dependency for getting DB session
async def get_db():
    async with async_session() as session:
        yield session
