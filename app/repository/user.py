from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate


async def get_user_by_email(db:AsyncSession, email:str):
    result=await db.execute(select(User).filter(User.email==email))
    return result.scalars().first()

async def create_user(db:AsyncSession,user:UserCreate):
    password=hash_password(user.password)
    new_user=User(
            username=user.username,
            email=user.email,
            hashed_password=password,
            
        )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

