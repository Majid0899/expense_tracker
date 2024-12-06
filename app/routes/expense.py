from typing import List
from fastapi import APIRouter, Depends, HTTPException,status
from app.db.session import get_db
from app.schemas.expense import ExpenseCreate,ExpenseResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_access_token
from app.models.expense import Expense
from app.repository.expense import create_expense,get_expense,fetch_expense

from app.repository.user import get_user_by_email
router=APIRouter()

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/create")
async def create(expense: ExpenseCreate,db:AsyncSession=Depends(get_db),token: str = Depends(oauth2_scheme)):
    try:
        user_email=decode_access_token(token)["sub"]
        user=await get_user_by_email(db,user_email)
        if not user:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )

        new_expense=await create_expense(db,expense,user.id)
        return new_expense
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
    

@router.get("/",response_model=List[ExpenseResponse])
async def show_expense(db:AsyncSession=Depends(get_db),token: str = Depends(oauth2_scheme)):

    try:
        user_email=decode_access_token(token)["sub"]
        user=await get_user_by_email(db,user_email)
        if not user:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
        expense=await get_expense(db,user.id)
        return expense
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
        
@router.put("/{expense_id}")
async def update(
    expense_id: int,
    expense: ExpenseCreate,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    
    try:
        user_email = decode_access_token(token)["sub"]
    
    
        user = await get_user_by_email(db, user_email)

        if not user:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )

    # Fetch the expense to update\

        existing_expense=await fetch_expense(db,user.id,expense_id)
    
        if not existing_expense:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Expense not found"
        )

    # Update the fields
        for key, value in expense.dict().items():
            setattr(existing_expense, key, value)
            
        db.add(existing_expense)
        await db.commit()
        await db.refresh(existing_expense)

        return {"message": "Expense updated successfully"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
        

@router.delete("/{expense_id}")
async def delete_expense(expense_id:int,db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)):

    try:
        user_email = decode_access_token(token)["sub"]
    
    
        user = await get_user_by_email(db, user_email)

        if not user:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )

    
        existing_expense=await fetch_expense(db,user.id,expense_id)
        if not existing_expense:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Expense not found"
        )
        await db.delete(existing_expense)
        await db.commit()
        return {"message": "Expense deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )

    
    