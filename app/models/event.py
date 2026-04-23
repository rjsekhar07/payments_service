from sqlalchemy import Column, String, DateTime, Float
from app.database import Base

class Event(Base):
    __tablename__ = "events"

    event_id = Column(String(100), primary_key=True)
    transaction_id = Column(String(50))
    event_type = Column(String(50))
    merchant_id = Column(String(50))
    amount = Column(Float)
    currency = Column(String(10))
    timestamp = Column(DateTime)