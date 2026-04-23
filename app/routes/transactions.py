from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models.transaction import Transaction

router = APIRouter()

@router.get("/transactions")
def get_transactions(
    merchant_id: str = None,
    status: str = None,
    start_date: datetime = Query(None, description="Start timestamp (ISO format)"),
    end_date: datetime = Query(None, description="End timestamp (ISO format)"),
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "timestamp",
    order: str = "desc",
    db: Session = Depends(get_db)
):
    query = db.query(Transaction)

    # Filtering
    if merchant_id:
        query = query.filter(Transaction.merchant_id == merchant_id)

    if status:
        query = query.filter(Transaction.status == status)

    # Date range filtering (using timestamp)
    if start_date:
        query = query.filter(Transaction.timestamp >= start_date)

    if end_date:
        query = query.filter(Transaction.timestamp <= end_date)

    # Sorting
    if sort_by == "timestamp":
        if order == "asc":
            query = query.order_by(Transaction.timestamp.asc())
        else:
            query = query.order_by(Transaction.timestamp.desc())

    total = query.count()

  
    transactions = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": transactions
    }