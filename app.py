from flask import Flask, render_template, request, redirect, url_for, session
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"

logging.basicConfig(level=logging.INFO)
jobstores = {"default": SQLAlchemyJobStore(url="sqlite:///jobs.sqlite")}
scheduler = BackgroundScheduler(jobstores=jobstores)
scheduler.start()

# Mock database for users and mailboxes
users = {}
mailboxes = {}

# Function to send an email
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
        return True
    except Exception as e:
        logging.error(f"Email send error: {e}")
        return False

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        users[username] = password
        mailboxes[username] = []
        return redirect(url_for("home"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and check_password_hash(users[username], password):
            session["username"] = username
            return redirect(url_for("dashboard"))
        return "Login failed"
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "username" in session:
        user_mailbox = mailboxes.get(session["username"], [])
        return render_template("dashboard.html", mailbox=user_mailbox)
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))

@app.route("/create_mail", methods=["POST"])
def create_mail():
    if "username" in session:
        mail_name = request.form["mail_name"]
        mailboxes[session["username"]].append(mail_name)
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
