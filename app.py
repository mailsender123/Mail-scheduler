from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
from zoneinfo import ZoneInfo
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import logging

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session management

# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Enable logging
logging.basicConfig(level=logging.INFO)

# Function to send an email using Gmail's SMTP server
def send_email(sender_email, sender_password, recipient_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Using SMTP_SSL for better compatibility with Render
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        logging.info("Email sent successfully.")
        return True
    except Exception as e:
        logging.error(f"Error sending email: {e}")
        return False

# Home route
@app.route("/")
def home():
    return render_template("home.html")

# Email scheduling route
@app.route("/schedule", methods=["GET", "POST"])
def schedule():
    if request.method == "POST":
        # Save sender info in session
        if "sender_email" not in session:
            session["sender_email"] = request.form["sender_email"]
            session["sender_password"] = request.form["sender_password"]
            return redirect(url_for("schedule"))

        data = request.form
        try:
            # Parse time and handle AM/PM conversion
            time_parts = list(map(int, data['time'].split(':')))
            ampm = data['ampm'].lower()
            if ampm == 'pm' and time_parts[0] != 12:
                time_parts[0] += 12
            elif ampm == 'am' and time_parts[0] == 12:
                time_parts[0] = 0

            # Create a datetime object with the specified date and time
            date_obj = datetime.strptime(data['date'], "%Y-%m-%d").replace(
                hour=time_parts[0], minute=time_parts[1], second=0
            )
            local_tz = ZoneInfo("Asia/Kolkata")
            date_obj = date_obj.replace(tzinfo=local_tz)

            # Ensure the chosen time is in the future
            if date_obj <= datetime.now(local_tz):
                return render_template("schedule.html", error="Choose a future time.")

            # Schedule the email
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
                id=f"{session['sender_email']}_{date_obj.timestamp()}"
            )
            logging.info("Email scheduled successfully.")
            return redirect(url_for('success'))
        except Exception as e:
            logging.error(f"Scheduling error: {e}")
            return render_template("schedule.html", error=str(e))

    return render_template("schedule.html")

# Success route
@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
