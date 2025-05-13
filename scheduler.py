from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, sender_password, recipient_email, subject, body):
    try:
        # Setting up the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        # Create the email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def schedule_email(sender_email, sender_password, recipient_email, subject, body, date, time_str):
    try:
        # Combine date and time for the trigger
        scheduled_datetime = datetime.strptime(f"{date} {time_str}", "%Y-%m-%d %H:%M")
        print(f"Scheduling email for {scheduled_datetime}")

        # Initialize scheduler
        scheduler = BackgroundScheduler()

        # Add the job to the scheduler with a DateTrigger
        scheduler.add_job(send_email, 
                          trigger=DateTrigger(run_date=scheduled_datetime), 
                          args=[sender_email, sender_password, recipient_email, subject, body], 
                          id=f"email_{scheduled_datetime}")

        # Start the scheduler if not already running
        if not scheduler.running:
            scheduler.start()
            print("Scheduler started.")

        return "Email scheduled successfully!"
    except Exception as e:
        return f"Error scheduling email: {e}"
