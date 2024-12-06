from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate

async def create_expense(db:AsyncSession,expense:ExpenseCreate,userId):
    new_expense=Expense(**expense.dict(),user_id=userId)
    db.add(new_expense)
    await db.commit()
    await db.refresh(new_expense)
    return new_expense

async def get_expense(db:AsyncSession,userId:int):
    query=await db.execute(select(Expense).filter(Expense.user_id==userId))
    return query.scalars().all()


async def fetch_expense(db:AsyncSession,userId:int,expense_id:int):
    query=await db.execute(
        select(Expense).filter(Expense.id == expense_id, Expense.user_id == userId),
    )
    existing_response=query.scalars().first()
    return existing_response
