from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from enum import Enum
from app.dependencies import get_db
from app.services.reconciliation import (
    get_reconciliation_summary,
    get_discrepancies
)

router = APIRouter()


# ✅ ENUM → Dropdown in Swagger
class DiscrepancyType(str, Enum):
    processed_not_settled = "processed_not_settled"
    failed_but_settled = "failed_but_settled"
    conflicting_transactions = "conflicting_transactions"


@router.get("/reconciliation/summary")
def summary(db: Session = Depends(get_db)):
    return get_reconciliation_summary(db)


@router.get("/reconciliation/discrepancies")
def discrepancies(
    type: DiscrepancyType = Query(
        None,
        description="Optional filter for discrepancy type"
    ),
    db: Session = Depends(get_db)
):
    return get_discrepancies(db, type)