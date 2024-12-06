from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.report import Report
from app.schemas.report import ReportCreate

from fastapi import APIRouter, Depends
from app.schemas.email import EmailSend
from app.repository.email import send_email as send_email_task

async def create_report(db: AsyncSession, report: ReportCreate,userId):
    new_report=Report(**report.dict(),user_id=userId)
    db.add(new_report)
    await db.commit()
    await db.refresh(new_report)
    return new_report

async def get_report(db: AsyncSession,userId):
    result = await db.execute(select(Report).filter(Report.user_id==userId))
    return result.scalars().all()
