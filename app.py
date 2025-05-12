from flask import Flask, request, redirect, url_for, render_template, flash
import os
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

@app.route('/schedule-email', methods=['POST'])
def schedule_email_route():
    sender_email = request.form.get("sender_email")
    sender_password = request.form.get("sender_password")
    recipient_email = request.form.get("recipient_email")
    subject = request.form.get("subject")
    body = request.form.get("body")
    date = request.form.get("date")
    time_str = request.form.get("time")
    am_pm = request.form.get("am_pm")

    message = schedule_email(sender_email, sender_password, recipient_email, subject, body, date, time_str, am_pm)
    flash(message)
    return redirect(url_for("success", message=message))

@app.route('/success')
def success():
    message = request.args.get('message', "Mail scheduled successfully")
    return render_template('success.html', message=message)

if __name__ == "__main__":
    app.run(debug=True)
