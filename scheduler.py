from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from email_sender import send_email

scheduler = BlockingScheduler()

def schedule_email(sender_email, sender_password, recipient_email, subject, body, date, time_str):
    try:
        # Combine date and time into a single datetime object
        scheduled_datetime = datetime.strptime(f"{date} {time_str}", "%Y-%m-%d %H:%M")

        # Scheduling the email
        scheduler.add_job(
            send_email,
            'date',
            run_date=scheduled_datetime,
            args=[sender_email, sender_password, recipient_email, subject, body],
            id=f"{sender_email}_{scheduled_datetime}"
        )
        print(f"Email scheduled successfully for {scheduled_datetime}")
        return f"Email scheduled successfully for {scheduled_datetime}"
    except Exception as e:
        print(f"Failed to schedule email: {e}")
        return f"Failed to schedule email: {e}"

def start_scheduler():
    try:
        print("Starting scheduler...")
        scheduler.start()
    except Exception as e:
        print(f"Error starting scheduler: {e}")
