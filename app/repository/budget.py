from sqlalchemy import select
from app.models.budget import Budget
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.budget import BudgetCreate

async def budget_create(db:AsyncSession,budget:BudgetCreate,userId):
    new_budget = Budget(**budget.dict(),user_id=userId)
    db.add(new_budget)
    await db.commit()
    await db.refresh(new_budget)
    return new_budget

async def budget_get(db:AsyncSession,userId):
    budget=await db.execute(select(Budget).filter(
        Budget.user_id==userId
    ))
    return budget.scalars().all()

async def fetch_budget(db:AsyncSession,userId,budget_id):
    query=await db.execute(
        select(Budget).filter(Budget.id == budget_id, Budget.user_id == userId),
    )
    existing_response=query.scalars().first()
    return existing_response 