from sqlalchemy import Column, Integer, Float, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    total = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    status = Column(String(20), default="completed")
    
    items = relationship("OrderItem", back_populates="order")
