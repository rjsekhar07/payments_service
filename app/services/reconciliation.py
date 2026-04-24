from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.transaction import Transaction
from app.models.event import Event


def get_reconciliation_summary(db: Session):
    result = db.query(
        Transaction.merchant_id,
        Transaction.status,
        func.count().label("count")
    ).group_by(
        Transaction.merchant_id,
        Transaction.status
    ).all()

    return [
        {
            "merchant_id": row[0],
            "status": row[1],
            "count": row[2]
        }
        for row in result
    ]


def get_conflicting_transactions(db: Session):
    result = db.query(
        Event.transaction_id,
        func.group_concat(Event.event_type).label("events")
    ).group_by(Event.transaction_id).all()

    conflicts = []

    for row in result:
        events = row.events.split(",")

        if (
            ("payment_failed" in events and "settled" in events) or
            ("payment_failed" in events and "payment_processed" in events)
        ):
            conflicts.append({
                "transaction_id": row.transaction_id,
                "events": events
            })

    return conflicts


def get_discrepancies(db: Session, type=None):
    # Subquery: settled transactions
    settled_txns = db.query(Event.transaction_id).filter(
        Event.event_type == "settled"
    ).subquery()

    # Case 1
    processed_not_settled = db.query(Event).filter(
        Event.event_type == "payment_processed",
        ~Event.transaction_id.in_(settled_txns)
    ).all()

    # Case 2
    failed_but_settled = db.query(Event).filter(
        Event.event_type == "payment_failed",
        Event.transaction_id.in_(settled_txns)
    ).all()

    # Case 3
    conflicting_transactions = get_conflicting_transactions(db)

    def serialize_events(events):
        return [
            {
                "event_id": e.event_id,
                "transaction_id": e.transaction_id,
                "event_type": e.event_type,
                "merchant_id": e.merchant_id,
                "amount": float(e.amount),
                "currency": e.currency,
                "timestamp": e.timestamp.isoformat()
            }
            for e in events
        ]

    result = {
        "processed_not_settled": serialize_events(processed_not_settled),
        "failed_but_settled": serialize_events(failed_but_settled),
        "conflicting_transactions": conflicting_transactions
    }

    # ✅ APPLY FILTER
    if type:
        return {type.value: result[type.value]}

    return result