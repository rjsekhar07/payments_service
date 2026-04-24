from fastapi import FastAPI
from app.routes import events, transactions, reconciliation
from app.database import Base, engine
from app.models import merchant, transaction, event

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Payment Reconciliation API is running"}

app.include_router(events.router)
app.include_router(transactions.router)
app.include_router(reconciliation.router)