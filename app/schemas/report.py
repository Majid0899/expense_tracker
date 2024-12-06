from pydantic import BaseModel
from datetime import date

class ReportBase(BaseModel):
    name: str
    start_date: date
    end_date: date
    description: str

class ReportCreate(ReportBase):
    pass

class ReportResponse(ReportBase):
    id: int

    class Config:
        from_attributes= True
