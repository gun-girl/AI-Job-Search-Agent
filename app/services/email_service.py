
import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()


def send_email(recipient: str, subject: str, body: str):
    host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    port = int(os.getenv("SMTP_PORT", "587"))
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    sender = os.getenv("SMTP_FROM_EMAIL") or username

    if not username or not password or not sender:
        raise RuntimeError("Gmail SMTP settings are incomplete.")

    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP(host, port, timeout=30) as smtp:
        smtp.starttls()
        smtp.login(username, password)
        smtp.send_message(message)


def send_test_email(recipient: str):
    send_email(
        recipient=recipient,
        subject="AI Job Search Agent - Test Email",
        body=(
            "Hello!\n\n"
            "Your AI Job Search Agent email configuration is working.\n\n"
            "This email was sent to the address saved in your profile.\n\n"
            "AI Job Search Agent"
        ),
    )
