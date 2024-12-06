from pydantic import BaseModel
from datetime import date as DateType
from typing import Optional



class ExpenseBase(BaseModel):
    amount: float
    category: str
    description: str
    date: DateType



class ExpenseCreate(ExpenseBase):
    pass

class ExpenseResponse(ExpenseBase):
    id: int
    class Config:
        from_attributes= True

class ExpenseUpdateResponse(BaseModel):
    message: str
    updated_expense: ExpenseResponse
    class Config:
        from_attributes = True
    

