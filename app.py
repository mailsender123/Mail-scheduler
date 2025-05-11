from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
from zoneinfo import ZoneInfo
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session management

# Initialize scheduler with async handling
scheduler = BackgroundScheduler()

async def start_scheduler():
    if not asyncio.get_event_loop().is_running():
        asyncio.set_event_loop(asyncio.new_event_loop())
    scheduler.start()

asyncio.run(start_scheduler())

# Function to send email
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
            server.send_message(msg)
        print(f"Email sent from {sender_email} to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Home route
@app.route("/")
def home():
    return render_template("home.html")

# Email scheduling route
@app.route("/schedule", methods=["GET", "POST"])
def schedule():
    if request.method == "POST":
        # Store sender info in session if not already done
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

            # Check if the chosen time is in the future
            if date_obj <= datetime.now(local_tz):
                return render_template("schedule.html", error="Choose a future time.")

            # Schedule the email sending
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
            return redirect(url_for("success"))
        except Exception as e:
            return render_template("schedule.html", error=str(e))
    return render_template("schedule.html")

# Success route
@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
