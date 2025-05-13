from flask import Flask, request, redirect, url_for, render_template, flash
import os
from scheduler import schedule_email

# Initialize the Flask app
app = Flask(__name__)
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
    time_str = request.form.get("time")  # Directly get the time input from the form

    try:
        # Schedule the email
        message = schedule_email(sender_email, sender_password, recipient_email, subject, body, date, time_str)
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
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
