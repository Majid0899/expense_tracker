from pydantic import BaseModel
from datetime import date

class IncomeBase(BaseModel):
    amount: float
    source: str
    description: str
    date: date

class IncomeCreate(IncomeBase):
    pass

class IncomeResponse(IncomeBase):
    id: int

    class Config:
        from_attributes = True
