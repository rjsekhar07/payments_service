from sqlalchemy import Column, String
from app.database import Base

class Merchant(Base):
    __tablename__ = "merchants"

    id = Column(String(50), primary_key=True)
    name = Column(String(100))