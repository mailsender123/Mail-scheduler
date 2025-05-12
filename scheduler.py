from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from email_sender import send_email
from zoneinfo import ZoneInfo
import logging

# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.start()

logging.basicConfig(level=logging.INFO)

def schedule_email(sender_email, sender_password, recipient_email, subject, body, date, time_str, am_pm):
    try:
        # Parsing date and time
        time_parts = [int(part) for part in time_str.split(':')]
        if am_pm.lower() == 'pm' and time_parts[0] != 12:
            time_parts[0] += 12
        elif am_pm.lower() == 'am' and time_parts[0] == 12:
            time_parts[0] = 0

        # Scheduling datetime with timezone using zoneinfo
        scheduled_datetime = datetime.strptime(date, "%Y-%m-%d").replace(
            hour=time_parts[0], minute=time_parts[1], second=0, tzinfo=ZoneInfo("Asia/Kolkata")
        )

        if scheduled_datetime <= datetime.now(ZoneInfo("Asia/Kolkata")):
            return "Scheduled time is in the past."

        scheduler.add_job(
            send_email,
            trigger=DateTrigger(run_date=scheduled_datetime),
            args=[sender_email, sender_password, recipient_email, subject, body],
            id=f"{sender_email}_{scheduled_datetime.timestamp()}"
        )
        return f"Email scheduled for {scheduled_datetime.strftime('%Y-%m-%d %I:%M %p')}."
    except Exception as e:
        logging.error(f"Error scheduling email: {e}")
        return f"Failed to schedule email: {e}"
