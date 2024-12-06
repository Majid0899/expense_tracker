from sqlalchemy import Column, Float, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Budget(Base):
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(20),)
    limit = Column(Float(20))
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="budgets")
