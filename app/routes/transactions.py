from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.dependencies import get_db
from app.models.transaction import Transaction
from app.models.event import Event

router = APIRouter()


@router.get("/transactions")
def get_transactions(
    merchant_id: str = Query(None, example="m_001"),
    status: str = Query(None, example="processed"),
    start_date: datetime = Query(
        None,
        description="Start timestamp (ISO format)",
        example="2026-04-01T00:00:00+00:00"
    ),
    end_date: datetime = Query(
        None,
        description="End timestamp (ISO format)",
        example="2026-04-03T00:00:00+00:00"
    ),
    skip: int = Query(0, example=0),
    limit: int = Query(10, example=10),
    sort_by: str = Query("timestamp", example="timestamp"),
    order: str = Query("desc", example="desc"),
    db: Session = Depends(get_db)
):
    query = db.query(Transaction).join(Event, Transaction.transaction_id == Event.transaction_id)

    # Filtering
    if merchant_id:
        query = query.filter(Transaction.merchant_id == merchant_id)

    if status:
        query = query.filter(Transaction.status == status)

    # Date range filtering
    if start_date:
        start_date = datetime.fromisoformat(start_date)
        query = query.filter(Event.timestamp >= start_date)

    if end_date:
        end_date = datetime.fromisoformat(end_date)
        query = query.filter(Event.timestamp <= end_date)

    # Sorting
    if sort_by == "timestamp":
        if order == "asc":
            query = query.order_by(Event.timestamp.asc())
        else:
            query = query.order_by(Event.timestamp.desc())

    total = query.count()

    transactions = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": transactions
    }

@router.get("/transactions/{txn_id}")
def get_transaction_by_id(txn_id: str, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.transaction_id == txn_id).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return transaction