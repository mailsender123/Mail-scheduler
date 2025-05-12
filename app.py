from flask import Flask, render_template, request, redirect, url_for
from scheduler import schedule_email

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/scheduler', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        sender_email = request.form['sender_email']
        sender_password = request.form['sender_password']
        recipient_email = request.form['recipient_email']
        subject = request.form['subject']
        body = request.form['body']
        date = request.form['date']
        time = request.form['time']
        am_pm = request.form['am_pm']

        result = schedule_email(sender_email, sender_password, recipient_email, subject, body, date, time, am_pm)
        return render_template('success.html', message=result)
    return render_template('schedule.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
