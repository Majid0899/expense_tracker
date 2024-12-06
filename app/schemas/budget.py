from pydantic import BaseModel

class BudgetBase(BaseModel):
    category: str
    limit: float

class BudgetCreate(BudgetBase):
    pass

class BudgetResponse(BudgetBase):
    id: int

    class Config:
        from_attributes= True
