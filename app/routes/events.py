from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.event import EventCreate
from app.dependencies import get_db
from app.services.event_service import process_event
from app.models.event import Event

router = APIRouter()

@router.post("/events")
def ingest_event(event: EventCreate, db: Session = Depends(get_db)):
    result = process_event(event, db)
    return {"status": result}

@router.get("/events/{event_id}")
def get_event_by_id(event_id: str, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.event_id == event_id).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    return event