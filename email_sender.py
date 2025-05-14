import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, sender_password, recipient_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        send=server.schedule_email(sender_email, sender_password, recipient_email, subject, body
with smtplib.SMTP('smtp.gmail.com', 587) as server:
            send.starttls()
            send.login(sender_email, sender_password)
            send.send_message(msg)
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
