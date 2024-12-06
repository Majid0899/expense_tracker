from sqlalchemy import Column, Float, String, Date, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Income(Base):
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float(20))
    source = Column(String(50))
    description = Column(String(50))
    date = Column(Date)
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="incomes")
