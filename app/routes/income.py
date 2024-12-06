from fastapi import APIRouter, Depends, HTTPException,status
from app.models.income import Income
from app.repository.user import get_user_by_email
from app.repository.income import create_income,get_income,fetch_income
from app.schemas.income import IncomeCreate,IncomeResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_access_token
from app.db.session import get_db
from typing import List

router=APIRouter()
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="auth/login")



@router.post("/create",response_model=IncomeResponse)
async def create_income(
    income:IncomeCreate,
    db:AsyncSession=Depends(get_db),
    token:str =Depends(oauth2_scheme)
):
    try:
        user_email=decode_access_token(token)["sub"]
        user=await get_user_by_email(db,user_email)
        if not user:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
        new_income=await create_income(db,income,user.id)
        return new_income
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )


@router.get("/",response_model=List[IncomeResponse])
async def show_income(
    db:AsyncSession=Depends(get_db),
    token:str =Depends(oauth2_scheme)
):
    try:
        user_email=decode_access_token(token)["sub"]
        user=await get_user_by_email(db,user_email)
        if not user:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
        income=await get_income(db,user.id)
        return income

        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )


@router.put("/{income_id}")
async def update_income(
    income_id:int,
    income:IncomeCreate,
    db:AsyncSession=Depends(get_db),
    token:str=Depends(oauth2_scheme)
):
    try:
        user_email=decode_access_token(token)["sub"]
        user=await get_user_by_email(db,user_email)
        if not user:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
        existing_income=await fetch_income(db,income_id,user.id);
        if not existing_income:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Income not found"
        )
        # Update the fields
        for key, value in income.dict().items():
            setattr(existing_income, key, value)
        db.add(existing_income)
        await db.commit()
        await db.refresh(existing_income)

        return {"message": "Income updated successfully"}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )

@router.delete("/{income_id}")
async def delete_income(income_id:int,db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)):

    try:
        user_email = decode_access_token(token)["sub"]
    
    
        user = await get_user_by_email(db, user_email)

        if not user:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )

    # Fetch the expense to update
        existing_income=await fetch_income(db,income_id,user.id)
        if not existing_income:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Income not found"
        )
        await db.delete(existing_income)
        await db.commit()
        return {"message": "Income deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
    
