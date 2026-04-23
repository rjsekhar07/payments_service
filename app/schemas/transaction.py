from pydantic import BaseModel
from datetime import datetime

class TransactionResponse(BaseModel):
    id: str
    merchant_id: str
    amount: float
    currency: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # for SQLAlchemy ORM