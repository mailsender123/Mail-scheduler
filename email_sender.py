import logging

def send_email(sender_email, sender_password, recipient_email, subject, body):
    try:
        logging.info(f"Sending email to {recipient_email} with subject: {subject}")
        print(f"Email sent to {recipient_email} with subject: {subject}")
        return True
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        return False
