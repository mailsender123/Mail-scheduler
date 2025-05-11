from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
from zoneinfo import ZoneInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging

# Set timezone explicitly for consistency
os.environ['TZ'] = 'Asia/Kolkata'

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Configure logging
logging.basicConfig(level=logging.INFO)

# Use AsyncIOScheduler for better performance on Render
scheduler = AsyncIOScheduler()
scheduler.start()

# Email sending function with detailed error logs
def send_email(sender_email, sender_password, recipient_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        
        logging.info(f"Email successfully sent from {sender_email} to {recipient_email}.")
        return True
    except Exception as e:
        logging.error(f"Failed to send email from {sender_email} to {recipient_email}. Error: {e}")
        return False

# Home page route
@app.route("/")
def home():
    return render_template("home.html")

# Email scheduling route
@app.route("/schedule", methods=["GET", "POST"])
def schedule():
    if request.method == "POST":
        if "sender_email" not in session:
            session["sender_email"] = request.form["sender_email"]
            session["sender_password"] = request.form["sender_password"]
            return render_template("schedule.html")

        data = request.form
        try:
            # Time parsing and AM/PM conversion
            time_parts = list(map(int, data['time'].split(':')))
            ampm = data['ampm'].lower()
            if ampm == 'pm' and time_parts[0] != 12:
                time_parts[0] += 12
            elif ampm == 'am' and time_parts[0] == 12:
                time_parts[0] = 0
            
            # Construct datetime object
            date_obj = datetime.strptime(data['date'], "%Y-%m-%d").replace(
                hour=time_parts[0], minute=time_parts[1], second=0
            )
            local_tz = ZoneInfo("Asia/Kolkata")
            date_obj = date_obj.replace(tzinfo=local_tz)

            # Validate the scheduled time
            if date_obj <= datetime.now(local_tz):
                logging.error("Scheduled time must be in the future.")
                return render_template("schedule.html", error="Choose a future time.")

            # Add the scheduled job
            scheduler.add_job(
                send_email,
                DateTrigger(run_date=date_obj),
                args=[
                    session["sender_email"],
                    session["sender_password"],
                    data['recipient_email'],
                    data['subject'],
                    data['body']
                ],
                id=f"{session['sender_email']}_{date_obj.timestamp()}",
                replace_existing=True
            )
            logging.info(f"Email scheduled successfully for {date_obj}.")
            return redirect(url_for('success'))
        except Exception as e:
            logging.error(f"Scheduling error: {e}")
            return render_template("schedule.html", error=str(e))
    return render_template("schedule.html")

# Success page route
@app.route("/success")
def success():
    return render_template("success.html")

# Run the app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
from zoneinfo import ZoneInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging

# Set timezone explicitly for consistency
os.environ['TZ'] = 'Asia/Kolkata'

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Configure logging
logging.basicConfig(level=logging.INFO)

# Use AsyncIOScheduler for better performance on Render
scheduler = AsyncIOScheduler()
scheduler.start()

# Email sending function with detailed error logs
def send_email(sender_email, sender_password, recipient_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        
        logging.info(f"Email successfully sent from {sender_email} to {recipient_email}.")
        return True
    except Exception as e:
        logging.error(f"Failed to send email from {sender_email} to {recipient_email}. Error: {e}")
        return False

# Home page route
@app.route("/")
def home():
    return render_template("home.html")

# Email scheduling route
@app.route("/schedule", methods=["GET", "POST"])
def schedule():
    if request.method == "POST":
        if "sender_email" not in session:
            session["sender_email"] = request.form["sender_email"]
            session["sender_password"] = request.form["sender_password"]
            return render_template("schedule.html")

        data = request.form
        try:
            # Time parsing and AM/PM conversion
            time_parts = list(map(int, data['time'].split(':')))
            ampm = data['ampm'].lower()
            if ampm == 'pm' and time_parts[0] != 12:
                time_parts[0] += 12
            elif ampm == 'am' and time_parts[0] == 12:
                time_parts[0] = 0
            
            # Construct datetime object
            date_obj = datetime.strptime(data['date'], "%Y-%m-%d").replace(
                hour=time_parts[0], minute=time_parts[1], second=0
            )
            local_tz = ZoneInfo("Asia/Kolkata")
            date_obj = date_obj.replace(tzinfo=local_tz)

            # Validate the scheduled time
            if date_obj <= datetime.now(local_tz):
                logging.error("Scheduled time must be in the future.")
                return render_template("schedule.html", error="Choose a future time.")

            # Add the scheduled job
            scheduler.add_job(
                send_email,
                DateTrigger(run_date=date_obj),
                args=[
                    session["sender_email"],
                    session["sender_password"],
                    data['recipient_email'],
                    data['subject'],
                    data['body']
                ],
                id=f"{session['sender_email']}_{date_obj.timestamp()}",
                replace_existing=True
            )
            logging.info(f"Email scheduled successfully for {date_obj}.")
            return redirect(url_for('success'))
        except Exception as e:
            logging.error(f"Scheduling error: {e}")
            return render_template("schedule.html", error=str(e))
    return render_template("schedule.html")

# Success page route
@app.route("/success")
def success():
    return render_template("success.html")

# Run the app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
