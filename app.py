from flask import Flask, request, redirect, url_for, render_template, flash
import os
from datetime import datetime
from scheduler import schedule_email

# Initialize the Flask app
app = Flask(__name__)

# Generate a random secret key programmatically
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/schedule')
def schedule():
    sender_email = request.args.get("sender_email")
    sender_password = request.args.get("sender_password")
    return render_template('schedule.html', sender_email=sender_email, sender_password=sender_password)

@app.route('/schedule_email', methods=['POST'])
def schedule_email_route():
    sender_email = request.form.get("sender_email")
    sender_password = request.form.get("sender_password")
    recipient_email = request.form.get("recipient_email")
    subject = request.form.get("subject")
    body = request.form.get("body")
    date = request.form.get("date")
    time_str = request.form.get("time")
    am_pm = request.form.get("am_pm")

    try:
        # Validate that all fields are filled
        if not all([sender_email, sender_password, recipient_email, subject, body, date, time_str, am_pm]):
            raise ValueError("All fields are required.")

        # Parsing date and time correctly
        try:
            time_parts = [int(part) for part in time_str.split(':')]
            if len(time_parts) != 2:
                raise ValueError("Invalid time format")
        except ValueError:
            raise ValueError("Time must be in HH:MM format")

        # Handling 12-hour format conversion correctly
        if am_pm.lower() == 'pm' and time_parts[0] != 12:
            time_parts[0] += 12
        elif am_pm.lower() == 'am' and time_parts[0] == 12:
            time_parts[0] = 0

        # Ensure hour and minute are within valid ranges
        if not (0 <= time_parts[0] <= 23):
            raise ValueError("Hour must be in 0..23")
        if not (0 <= time_parts[1] <= 59):
            raise ValueError("Minute must be in 0..59")

        # Check if the scheduled time is in the past
        scheduled_datetime = datetime.strptime(f"{date} {time_parts[0]:02d}:{time_parts[1]:02d}", "%Y-%m-%d %H:%M")
        if scheduled_datetime <= datetime.now():
            raise ValueError("Scheduled time is in the past.")

        # Schedule the email
        message = schedule_email(sender_email, sender_password, recipient_email, subject, body, date, time_str, am_pm)
        flash(message)
        return redirect(url_for("success", message=message))

    except Exception as e:
        error_message = f"Error scheduling email: {e}"
        flash(error_message)
        return redirect(url_for("success", message=error_message))

@app.route('/success')
def success():
    message = request.args.get('message', "Mail scheduled successfully")
    return render_template('success.html', message=message)

if __name__ == "__main__":
    # Run the app, allowing flexible debug mode based on environment variable
    app.run(host="0.0.0.0", port=5000, debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
