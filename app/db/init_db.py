import asyncio
from app.db.session import engine
from app.models import user, expense, income, budget, report  # Import all models
from app.db.base_class import Base

# Create tables
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Main function to run table creation
if __name__ == "__main__":
    asyncio.run(init_db())
