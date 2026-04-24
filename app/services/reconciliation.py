from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db

router = APIRouter()

@router.get("/reconciliation/discrepancies")
def get_discrepancies(
    type: str = Query(
        None,
        description="Optional. Filter by discrepancy type. Allowed values: processed_not_settled, failed_but_settled, conflicting_transactions",
        example="processed_not_settled"
    ),
    db: Session = Depends(get_db)
):
    valid_types = [
        "processed_not_settled",
        "failed_but_settled",
        "conflicting_transactions"
    ]

    if type and type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid type. Allowed values: {valid_types}"
        )
    
    discrepancies = []

    processed_not_settled = []  
    failed_but_settled = []
    conflicting_transactions = []

    if type == "processed_not_settled":
        discrepancies = processed_not_settled

    elif type == "failed_but_settled":
        discrepancies = failed_but_settled

    elif type == "conflicting_transactions":
        discrepancies = conflicting_transactions

    else:
        
        discrepancies = {
            "processed_not_settled": processed_not_settled,
            "failed_but_settled": failed_but_settled,
            "conflicting_transactions": conflicting_transactions
        }

    return discrepancies