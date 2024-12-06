from fastapi import APIRouter,status,HTTPException,Depends
from app.core.custom_form import OAuth2PasswordRequestFormEmail
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import UserResponse,UserCreate,UserLogin
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repository.user import get_user_by_email,create_user
from app.core.security import create_access_token,verify_password


router=APIRouter()


@router.post("/register",response_model=UserResponse)
async def register(user:UserCreate,db:AsyncSession=Depends(get_db)):
    # Check Email Already Exist or not
    try:
        existing_email=await get_user_by_email(db,user.email)
        if existing_email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

        new_user=await create_user(db,user)
        return new_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )


@router.post("/login")
async def login(form_data:OAuth2PasswordRequestForm = Depends(),db:AsyncSession=Depends(get_db)):
    try:
        user=await get_user_by_email(db,form_data.username)
        if not user or not verify_password(form_data.password,user.hashed_password) :
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
        access_token=create_access_token({"sub":user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )