from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.income import Income
from app.schemas.income import IncomeCreate

async def create_income(db:AsyncSession,income:IncomeCreate,userId):
    income_create=Income(**income.dict(),user_id=userId)
    db.add(income_create)
    await db.commit()
    await db.refresh(income_create)
    return income_create

async def get_income(db:AsyncSession,userId):
    income=await db.execute(select(Income).filter(Income.user_id==userId))
    income=income.scalars().all()
    return income


async def fetch_income(db:AsyncSession,income_id,userId):
    query=await db.execute(
        select(Income).filter(Income.id == income_id, Income.user_id == userId),
    )
    existing_response=query.scalars().first()
    return existing_response