from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.db.models import Base
from app.db.sample_data import load_sample_data
from app.services.report_service import generate_report

DATABASE_URL = "sqlite:///./sample.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)  # Create tables

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def init_data():
    db = SessionLocal()
    load_sample_data(db)

@app.get("/api/report")
def get_weekly_report(db: Session = Depends(get_db)):
    return generate_report(db)
