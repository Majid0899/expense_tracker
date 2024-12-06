from sqlalchemy import  Column, Integer, String
from app.db.base_class import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), unique=True, index=True,nullable=False)
    email = Column(String(50), unique=True, index=True,nullable=False)
    hashed_password = Column(String(255),nullable=False)

    # Relationships
    incomes = relationship("Income", back_populates="user")
    expenses = relationship("Expense", back_populates="user")
    budgets = relationship("Budget", back_populates="user")
    reports = relationship("Report", back_populates="user")

    
