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
        send_email("mukilarasu0923@gmail.com", subject, body)

        logging.info("✅ Report successfully sent to mukilarasu0923@gmail.com")

    except Exception as e:
        logging.error(f"❌ Error while sending weekly report: {e}")

# ====================================================================================================================================================
#                    This is the old code for the scheduler which was running every Monday at 10:00 AM
# ====================================================================================================================================================


# def start_scheduler():
#     scheduler = BackgroundScheduler(timezone="Asia/Kolkata")  # Optional: set your local timezone
#     scheduler.add_job(
#         scheduled_weekly_report,
#         trigger='cron',
#         day_of_week='mon',
#         hour=10,
#         minute=0,
#         id="weekly_report_job"
#     )
#     scheduler.start()
#     logging.info("🗓️ Scheduler started (Every Monday @ 10:00 AM)")
# ====================================================================================================================================================



# ====================================================================================================================================================
#                    This is the new Testing code for the scheduler which is running every day at 2:28 PM
# ====================================================================================================================================================

def start_scheduler():
    scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
    scheduler.add_job(
        scheduled_weekly_report,
        trigger='cron',
        day_of_week='mon-sun',  # Every day (so it's not limited to Monday)
        hour=13,                 # 2 PM - 14 # 1 PM - 13
        minute=46,               # Change to next minute from current time # 35
        id="test_report_job"
    )
    scheduler.start()
    logging.info("⏱️ One-time Scheduler started (e.g., today @ 1:46 PM)")

# ====================================================================================================================================================