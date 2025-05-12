from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from email_sender import send_email
from flask import flash, redirect, url_for, current_app
from datetime import datetime
from zoneinfo import ZoneInfo
import logging
import atexit
from uuid import uuid4

scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

def schedule_email(sender_email, sender_password, recipient_email, subject, body, date, time_str, am_pm):
    try:
        time_parts = [int(part) for part in time_str.split(':')]
        if am_pm.lower() == 'pm' and time_parts[0] != 12:
            time_parts[0] += 12
        elif am_pm.lower() == 'am' and time_parts[0] == 12:
            time_parts[0] = 0

        scheduled_datetime = datetime.strptime(date, "%Y-%m-%d").replace(
            hour=time_parts[0], minute=time_parts[1], second=0, tzinfo=ZoneInfo("Asia/Kolkata")
        )

        if scheduled_datetime <= datetime.now(ZoneInfo("Asia/Kolkata")):
            flash("Scheduled time is in the past.")
            return "Failed to schedule mail: Time is in the past"

        job_id = f"{sender_email}_{scheduled_datetime.timestamp()}_{uuid4()}"

        def job_wrapper():
            result = send_email(sender_email, sender_password, recipient_email, subject, body)
            with current_app.app_context():
                if result:
                    flash("Mail sent successfully")
                    logging.info("Email sent successfully.")
                else:
                    flash("Failed to send mail")
                    logging.error("Email sending failed.")

        scheduler.add_job(
            job_wrapper,
            trigger=DateTrigger(run_date=scheduled_datetime),
            id=job_id,
            replace_existing=True,
            misfire_grace_time=300
        )

        logging.info("Email scheduled successfully.")
        return "Mail scheduled successfully"
    except Exception as e:
        logging.error(f"Error scheduling email: {e}")
        return f"Error scheduling email: {e}"
