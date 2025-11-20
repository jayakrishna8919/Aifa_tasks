from email.message import EmailMessage
from config.config import SMTP_SERVER,SMTP_PORT,SMTP_USER,SMTP_PASSWORD
import smtplib
def send_email_sync(to: str, subject: str, body: str):
    msg = EmailMessage()
    msg["From"] = SMTP_USER
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)


    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASSWORD)
        smtp.send_message(msg)
