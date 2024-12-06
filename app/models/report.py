from sqlalchemy import Column, Integer, String, Date,ForeignKey
from app.db.base_class import Base
from sqlalchemy.orm import relationship

class Report(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30))
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(String(50))
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="reports")
