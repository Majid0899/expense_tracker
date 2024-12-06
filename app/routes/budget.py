from typing import List
from fastapi import APIRouter, Depends, HTTPException,status
from app.db.session import get_db
from app.repository.budget import budget_create, budget_get, fetch_budget
from app.schemas.budget import BudgetCreate,BudgetResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_access_token
from app.repository.user import get_user_by_email

router=APIRouter()

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post("/create")
async def create_budget(budget: BudgetCreate,db:AsyncSession=Depends(get_db),token:str=Depends(oauth2_scheme)):
    try:
        user_email=decode_access_token(token)["sub"]
        user=await get_user_by_email(db,user_email)
        if not user:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
        new_budget=await budget_create(db,budget,user.id)
        return new_budget
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )

@router.get("/",response_model=List[BudgetResponse])
async def get_budget(db:AsyncSession=Depends(get_db),token:str=Depends(oauth2_scheme)):
    try:
        user_email=decode_access_token(token)["sub"]
        user=await get_user_by_email(db,user_email)
        if not user:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    
        budget=await budget_get(db,user.id)
        return budget
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )

@router.put("/{budget_id}")
async def update_budget(budget_id:int,limit:float,db:AsyncSession=Depends(get_db),token:str=Depends(oauth2_scheme)):
    try:
        user_email = decode_access_token(token)["sub"]
        user = await get_user_by_email(db, user_email)
        if not user:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )

        existing_budget=await fetch_budget(db,user.id,budget_id)
        if not existing_budget:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Budget not found"
        )
        existing_budget.limit=limit
        db.add(existing_budget)
        await db.commit()
        await db.refresh(existing_budget)
        return {"Budget Upated Successfully"} 
    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )


@router.delete("/{budget_id}")
async def delete_budget(budget_id:int,db:AsyncSession=Depends(get_db),token:str=Depends(oauth2_scheme)):
    try:
        user_email = decode_access_token(token)["sub"]
        user = await get_user_by_email(db, user_email)
        if not user:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )

        existing_budget=await fetch_budget(db,user.id,budget_id)
        if not existing_budget:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Budget not found"
        )
        await db.delete(existing_budget)
        await db.commit()
        return {"message": "Budget deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )