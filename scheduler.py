from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from email_sender import send_email
from zoneinfo import ZoneInfo
from datetime import datetime
from uuid import uuid4
import logging
import atexit

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize and start the scheduler
scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

def schedule_email(sender_email, sender_password, recipient_email, subject, body, date, time_str, am_pm):
    try:
        # Parse time
        time_parts = [int(part) for part in time_str.split(':')]
        if am_pm.lower() == 'pm' and time_parts[0] != 12:
            time_parts[0] += 12
        elif am_pm.lower() == 'am' and time_parts[0] == 12:
            time_parts[0] = 0

        # Calculate the scheduled datetime
        scheduled_datetime = datetime.strptime(date, "%Y-%m-%d").replace(
            hour=time_parts[0], minute=time_parts[1], second=0, tzinfo=ZoneInfo("Asia/Kolkata")
        )
        
        if scheduled_datetime <= datetime.now(ZoneInfo("Asia/Kolkata")):
            return "Scheduled time is in the past."

        job_id = f"{sender_email}_{scheduled_datetime.timestamp()}_{uuid4()}"
        scheduler.add_job(
            send_email,
            trigger=DateTrigger(run_date=scheduled_datetime),
            args=[sender_email, sender_password, recipient_email, subject, body],
            id=job_id,
            replace_existing=True,
            misfire_grace_time=300
        )
        logging.info(f"Email scheduled: {job_id} at {scheduled_datetime}")
        return f"Email scheduled for {scheduled_datetime.strftime('%Y-%m-%d %I:%M %p')}."
    except Exception as e:
        logging.error(f"Error scheduling email: {e}")
        return f"Failed to schedule email: {e}"
