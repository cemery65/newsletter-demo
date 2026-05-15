import os
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587


def send_email(to: str, sender: str, subject: str, html_body: str) -> None:
    smtp_user = os.getenv("GMAIL_SMTP_USER")
    smtp_password = os.getenv("GMAIL_SMTP_PASSWORD")

    if not smtp_user or not smtp_password:
        raise ValueError("GMAIL_SMTP_USER and GMAIL_SMTP_PASSWORD must be set in .env")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(sender, to, msg.as_string())

    print(f"Email sent to {to}")


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python send_gmail.py <to> <from> <subject> <html_body>")
        sys.exit(1)
    send_email(
        to=sys.argv[1],
        sender=sys.argv[2],
        subject=sys.argv[3],
        html_body=sys.argv[4],
    )
