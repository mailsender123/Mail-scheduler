from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
from zoneinfo import ZoneInfo
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session management

scheduler = BackgroundScheduler()
scheduler.start()

# Function to send email (stub for demonstration)
def send_email(sender_email, sender_password, recipient_email, subject, body):
    print(f"Email scheduled from {sender_email} to {recipient_email} with subject '{subject}'.")

# Home route
@app.route("/")
def home():
    return render_template("home.html")

# Email scheduling route
@app.route("/schedule", methods=["GET", "POST"])
def schedule():
    if request.method == "POST":
        # Check if sender info is not already in session
        if "sender_email" not in session:
            session["sender_email"] = request.form["sender_email"]
            session["sender_password"] = request.form["sender_password"]
            return render_template("schedule.html")

        data = request.form
        try:
            # Parse time and handle AM/PM conversion
            time_parts = list(map(int, data['time'].split(':')))
            ampm = data['ampm'].lower()
            if ampm == 'pm' and time_parts[0] != 12:
                time_parts[0] += 12
            elif ampm == 'am' and time_parts[0] == 12:
                time_parts[0] = 0

            # Validate hour range
            if not (0 <= time_parts[0] <= 23):
                raise ValueError("Hour must be in 0..23")

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
                id=f"{session['sender_email']}_{date_obj.timestamp()}"
            )
            return redirect(url_for('success'))
        except Exception as e:
            return render_template("schedule.html", error=str(e))
    return render_template("schedule.html")

# Success route
@app.route("/success")
def success():
    return render_template("success.html")

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
