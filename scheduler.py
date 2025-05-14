from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from email_sender import send_email

scheduler = BackgroundScheduler()
scheduler.start()

def schedule_email(sender_email, sender_password, recipient_email, subject, body, date, time_str):
    try:
        scheduled_datetime = datetime.strptime(f"{date} {time_str}", "%Y-%m-%d %H:%M")
        job_id = f"{sender_email}_{scheduled_datetime.strftime('%Y%m%d%H%M%S')}"

        # Adding the email sending job to the scheduler
        scheduler.add_job(
            send_email,
            'date',
            run_date=scheduled_datetime,
            args=[sender_email, sender_password, recipient_email, subject, body],
            id=job_id
        )
        print(f"Email scheduled for: {scheduled_datetime}")
        return f"Email scheduled successfully for {scheduled_datetime}"
    except Exception as e:
        print(f"Error scheduling email: {e}")
        return f"Error: {e}"
