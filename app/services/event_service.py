from app.models.event import Event
from app.models.transaction import Transaction
from app.models.merchant import Merchant
from app.utils.constants import STATUS_PRIORITY
from datetime import datetime

def process_event(event, db):

    # 1. Idempotency check
    existing = db.query(Event).filter_by(event_id=event.event_id).first()
    if existing:
        return "duplicate"

    # 2. Save event
    db_event = Event(
    event_id=event.event_id,
    transaction_id=event.transaction_id,
    event_type=event.event_type,
    merchant_id=event.merchant_id,
    amount=event.amount,
    currency=event.currency,
    timestamp=event.timestamp
)
    db.add(db_event)

    # 3. Merchant upsert
    merchant = db.query(Merchant).filter_by(id=event.merchant_id).first()
    if not merchant:
        merchant = Merchant(
            id=event.merchant_id,
            name=event.merchant_name
        )
        db.add(merchant)

    # 4. Transaction upsert
    txn = db.query(Transaction).filter_by(id=event.transaction_id).first()

    if not txn:
        txn = Transaction(
            id=event.transaction_id,
            merchant_id=event.merchant_id,
            amount=event.amount,
            currency=event.currency,
            status=event.event_type,
            created_at=event.timestamp
        )
        db.add(txn)
    else:
        # handle ordering
        if STATUS_PRIORITY[event.event_type] > STATUS_PRIORITY[txn.status]:
            txn.status = event.event_type
            txn.updated_at = datetime.utcnow()

    db.commit()
    return "processed"