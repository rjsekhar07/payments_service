from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.services.reconciliation import (
    get_reconciliation_summary,
    get_discrepancies
)

router = APIRouter()


@router.get("/reconciliation/summary")
def summary(db: Session = Depends(get_db)):
    return get_reconciliation_summary(db)


@router.get("/reconciliation/discrepancies")
def discrepancies(db: Session = Depends(get_db)):
    return get_discrepancies(db)