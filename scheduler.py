from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from email_sender import send_email

scheduler = BackgroundScheduler()
scheduler.start()

def schedule_email(sender_email, sender_password, recipient_email, subject, body, date, time_str):
    try:
        # Combine date and time into a single datetime object
        scheduled_datetime = datetime.strptime(f"{date} {time_str}", "%Y-%m-%d %H:%M")

        # Scheduling the email
        job = scheduler.add_job(
            send_email,
            'date',
            run_date=scheduled_datetime,
            args=[sender_email, sender_password, recipient_email, subject, body]
        )
        return f"Email scheduled successfully for {scheduled_datetime}"
    except Exception as e:
        return f"Failed to schedule email: {e}"
