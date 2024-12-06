from typing import List
from fastapi import APIRouter,HTTPException,status,Depends
from fastapi.security import OAuth2PasswordBearer
from app.schemas.report import ReportCreate,ReportResponse
from app.core.security import decode_access_token
from app.repository.user import get_user_by_email
from app.repository.report import create_report,get_report
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.report import Report
from app.schemas.email import EmailSend
from app.repository.email import send_email as send_email_task


router=APIRouter()
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="auth/login")



@router.post("/create")
async def report_create(report:ReportCreate,db:AsyncSession=Depends(get_db),token:str=Depends(oauth2_scheme)):
    try:
        user_email=decode_access_token(token)["sub"]
        user=await get_user_by_email(db,user_email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
        new_report=await create_report(db,report,user.id)
        return new_report
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={str(e)}
        )
@router.get("/",response_model=List[ReportResponse])
async def get_reports(db:AsyncSession=Depends(get_db),token:str=Depends(oauth2_scheme)):
    try:
        user_email=decode_access_token(token)["sub"]
        user=await get_user_by_email(db,user_email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
        report= await get_report(db,user.id)
        
        email_message = f"Dear {user.email},\n\nHere is your requested report:\n\n{report}"
        email_data = EmailSend(
        recipient=user.email,
        subject="Your Expense Report",
        message=email_message
    )

    
        await send_email_task(email_data)
        return report
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={str(e)}
        )

