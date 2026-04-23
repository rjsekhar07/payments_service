from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.event import EventCreate
from app.dependencies import get_db
from app.services.event_service import process_event

router = APIRouter()

@router.post("/events")
def ingest_event(event: EventCreate, db: Session = Depends(get_db)):
    result = process_event(event, db)
    return {"status": result}