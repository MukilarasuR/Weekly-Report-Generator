from apscheduler.schedulers.background import BackgroundScheduler
from app.services.report_service import generate_report
from app.utils.gmail_sender import send_email
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
import logging

# Setup logging
logging.basicConfig(
    format="%(asctime)s — %(levelname)s — %(message)s",
    level=logging.INFO
)

def scheduled_weekly_report():
    logging.info("⏰ Running scheduled weekly report job...")
    try:
        db: Session = SessionLocal()
        report_data = generate_report(db, channel="gmail")
        subject = "📊 Weekly Report – Mall Construction"
        body = report_data["report"]

        # You can fetch manager's email dynamically if needed
        send_email("manager@example.com", subject, body)

        logging.info("✅ Report successfully sent to manager@example.com")

    except Exception as e:
        logging.error(f"❌ Error while sending weekly report: {e}")

def start_scheduler():
    scheduler = BackgroundScheduler(timezone="Asia/Kolkata")  # Optional: set your local timezone
    scheduler.add_job(
        scheduled_weekly_report,
        trigger='cron',
        day_of_week='mon',
        hour=10,
        minute=0,
        id="weekly_report_job"
    )
    scheduler.start()
    logging.info("🗓️ Scheduler started (Every Monday @ 10:00 AM)")



# from apscheduler.schedulers.background import BackgroundScheduler
# from app.services.report_service import generate_report
# from app.utils.gmail_sender import send_email
# from sqlalchemy.orm import Session
# from app.db.database import SessionLocal

# def scheduled_weekly_report():
#     db: Session = SessionLocal()
#     report_data = generate_report(db, channel="gmail")
#     subject = f"📊 Weekly Report – Mall Construction"
#     body = report_data["report"]
#     send_email("manager@example.com", subject, body)  # Replace with actual manager email

# def start_scheduler():
#     scheduler = BackgroundScheduler()
#     # Every Monday at 10:00 AM
#     scheduler.add_job(scheduled_weekly_report, 'cron', day_of_week='mon', hour=10, minute=0)
#     scheduler.start()
