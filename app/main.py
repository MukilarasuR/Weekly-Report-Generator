from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from app.db.models import Base
from app.db.sample_data import load_sample_data
from app.services.report_service import generate_report
from app.db.database import SessionLocal, get_db

from app.scheduler import start_scheduler

app = FastAPI()

@app.on_event("startup")
def init_data():
    db = SessionLocal()
    load_sample_data(db)
    start_scheduler()  # Start the background job on startup

@app.get("/api/report")
def get_weekly_report(
    channel: str = Query("gmail", enum=["gmail", "outlook", "whatsapp"]),
    db: Session = Depends(get_db)
):
    return generate_report(db, channel)
