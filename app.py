from flask import Flask, request, redirect, url_for, render_template, flash
from scheduler import schedule_email
import os

# Hard-coded credentials and configurations
SECRET_KEY = "your_secret_key"  # Replace with any random string
SENDER_EMAIL = "mailscheduler030@gmail.com"
SENDER_PASSWORD = "boom cggz kbxr fikz"  # Replace with your App Password

# Initialize the Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/schedule')
def schedule():
    return render_template('schedule.html')

@app.route('/schedule-email', methods=['POST'])
def schedule_email_route():
    recipient_email = request.form.get("recipient_email")
    subject = request.form.get("subject")
    body = request.form.get("body")
    date = request.form.get("date")
    time_str = request.form.get("time")

    try:
        # Schedule the email
        message = schedule_email(SENDER_EMAIL, SENDER_PASSWORD, recipient_email, subject, body, date, time_str)
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
    app.run(debug=True, host="0.0.0.0", port=5000)
